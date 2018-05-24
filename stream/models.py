from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

STREAM_TAGS = (
    (0, 'Guest'),
    (1, 'Sponsor'),
    (2, 'Player'),
    (3, 'Main'),
)


class Category(models.Model):
    name = models.CharField(max_length=50)
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


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
        null=True
    )
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.username


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
    description = models.CharField(max_length=50, blank=True, null=True)
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

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
    title = models.CharField(max_length=50)
    URL = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    tag = models.IntegerField(choices=STREAM_TAGS, default=0)
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


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
    when = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.username

    def is_reported(self, user):
        content_type = ContentType.objects.get_for_model(self)
        return Report.objects.filter(
            reporter=user, content_type=content_type,
            content_id=self.id).exists()


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

    def __str__(self):
        return self.member.owner.username


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
        null=True)
    content_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'content_id')
    reason = models.CharField(choices=REASONS, max_length=50)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return '{} reported {} of id {}'.format(
            self.reporter.username, self.content_type, self.content_id)
