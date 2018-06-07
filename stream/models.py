from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=50)
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


REASONS = (
    (0, "Pornographic content."),
    (1, "Copyright infringement."),
    (2, "Racist content."))


class Report(models.Model):
    reporter = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reported_comments')
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        null=True, related_name='reports')
    content_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'content_id')
    when = models.DateTimeField(auto_now_add=True, null=True)
    reason = models.IntegerField(choices=REASONS)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return '{} reported {} of id {}'.format(
            self.reporter.username, self.content_type, self.content_id)

    @property
    def get_reason(self):
        return REASONS[int(self.reason)][1]


NOTIFICATION_TEMPLATES = (
    # Profile
    (0, '{target.owner.username} has subscribed to you'),

    # Stream
    (1, '{target.owner.username} has started a stream: \
        {target.title} in {target.lobby.name}'),
    (2, 'Your stream has been updated as {target.get_tag}'),
    # Reported Stream
    (3, 'Your stream has been removed due to {target.get_reason}'),

    # Lobby
    (4, '{target.owner.username} has created a lobby: {target.name}'),
    # LobbyMembership
    (5, 'You have been accepted as a member in the lobby: \
        {target.lobby.name}'),
    (6, 'You have been rejected as a member in the lobby: \
        {target.lobby.name}'),

    # Comment
    (7, '{target.owner.username} has commented in lobby: {target.lobby.name}'),
    # Reported Comment
    (8, 'Your comment has been removed due to {target.get_reason}'),
)


class Notification(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True
    )

    target_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        null=True, related_name='notifications')
    target_id = models.PositiveIntegerField(null=True)
    target_object = GenericForeignKey('target_type', 'target_id')

    template = models.IntegerField(choices=NOTIFICATION_TEMPLATES)

    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    @property
    def get_notification(self):
        return NOTIFICATION_TEMPLATES[int(
            self.template)][1].format(target=self.target_object)

    def __str__(self):
        return '{} was notified about: {} with target id: {}'.format(
            self.owner.username, self.target_type, self.target_id)


class Profile(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    nickname = models.CharField(max_length=50)
    avatar = models.ImageField(
        upload_to='stream/static/images',
        blank=True,
        null=True,
        default='stream/static/images/default_avatar.png'
    )
    notify = GenericRelation(
        Notification,
        related_query_name='profile',
        content_type_field="target_type",
        object_id_field="target_id"
    )
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(owner=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def is_viewed(self, lobby):
        return LobbyViews.objects.filter(viewer=self, lobby=lobby).exists()

    def is_subscribed(self, user):
        """
        Checks if there exists a subscription wherein the
        current user is subscribed to the streamer owning
        this profile. Returns boolean value.
        """
        return Subscription.objects.filter(
            subscriber=user, publisher=self.owner).exists()

    def __str__(self):
        return self.owner.username


LOBBY_TYPE = (
    (0, "Public"),
    (1, "Private")
)


class Lobby(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lobbies',
        null=True
    )
    name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to='stream/static/images',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='lobby'
    )
    notify = GenericRelation(
        Notification,
        related_query_name='lobbies',
        content_type_field="target_type",
        object_id_field="target_id"
    )
    description = models.CharField(max_length=50, blank=True, null=True)
    lobby_type = models.IntegerField(choices=LOBBY_TYPE, default=0)
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    def is_moderator(self, user):
        return Moderator.objects.filter(
            lobby=self, owner=user, removed=False).exists()

    def is_member(self, user):
        return LobbyMembership.objects.filter(
            lobby=self, member=user, status=2, removed=False).exists()

    def has_stream(self, user):
        return self.streams.filter(owner=user, removed=False)

    def has_main(self):
        return self.streams.filter(tag=3, removed=False).exists()

    def get_main(self):
        return self.streams.get(tag=3, removed=False)

    def is_private(self):
        flag = False
        if self.lobby_type == 1:
            flag = True
        return flag

    def __str__(self):
        return self.name


class Moderator(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='moderators'
    )
    lobby = models.ForeignKey(
        Lobby,
        on_delete=models.CASCADE,
        related_name='moderators'
    )
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.username


STREAM_TAGS = (
    (0, 'Guest'),
    (1, 'Sponsor'),
    (2, 'Player'),
    (3, 'Main'),
)


class Stream(models.Model):
    lobby = models.ForeignKey(
        Lobby,
        on_delete=models.CASCADE,
        related_name='streams'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='streams'
    )
    image = models.ImageField(
        upload_to='stream/static/images',
        blank=True,
        null=True
    )
    notify = GenericRelation(
        Notification,
        related_query_name='streams',
        content_type_field="target_type",
        object_id_field="target_id"
    )
    title = models.CharField(max_length=50)
    URL = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    session_id = models.CharField(max_length=200, default="")
    pub_token = models.CharField(max_length=400, default="")
    sub_token = models.CharField(max_length=400, default="")
    tag = models.IntegerField(choices=STREAM_TAGS, default=0)
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def get_tag(self):
        return STREAM_TAGS[int(self.tag)][1]


class Comment(models.Model):
    text = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    lobby = models.ForeignKey(
        Lobby,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True
    )
    report = GenericRelation(
        Report,
        related_query_name='comments',
        content_type_field="content_type",
        object_id_field="content_id"
    )
    notify = GenericRelation(
        Notification,
        related_query_name='comments',
        content_type_field="target_type",
        object_id_field="target_id"
    )
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.username

    def is_reported(self, user):
        content_type = ContentType.objects.get_for_model(self)
        return Report.objects.filter(
            reporter=user, content_type=content_type,
            content_id=self.id).exists()

    @property
    def reported(self):
        content_type = ContentType.objects.get_for_model(self)
        return Report.objects.filter(
            content_type=content_type, content_id=self.id).exists()


STATUS = (
    (0, 'PENDING'),
    (1, 'REJECTED'),
    (2, 'ACCEPTED'),
)


class LobbyMembership(models.Model):
    member = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    lobby = models.ForeignKey(
        Lobby,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    status = models.IntegerField(choices=STATUS, default=0)
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    PENDING = 0
    REJECTED = 1
    ACCEPTED = 2

    def is_moderator(self):
        return Moderator.objects.filter(
            lobby=self.lobby, owner=self.member.owner, removed=False).exists()

    def __str__(self):
        return self.member.owner.username


class LobbyViews(models.Model):
    viewer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='views'
    )
    lobby = models.ForeignKey(
        Lobby,
        on_delete=models.CASCADE,
        related_name='views'
    )
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.viewer.owner.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name="subscribers")
    publisher = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name="publishers")

    def __str__(self):
        return ("{} is subscribed to {}").format(
            self.subscriber, self.publisher)


class Favorite(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites")
    lobby = models.ForeignKey(
        Lobby, on_delete=models.CASCADE, related_name="favorites")
    when = models.DateTimeField(auto_now_add=True, null=True)
