from stream import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(
            owner=instance,
            nickname=instance.username
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=models.Subscription)
def create_notify_subscribe(sender, instance, created, **kwargs):
    if created:
        models.Notification.objects.create(
            owner=instance.publisher,
            template=0,
            target_id=instance.subscriber.profile.pk,
            target_type=ContentType.objects.get_for_model(models.Profile),
            target_object=instance.subscriber.profile
        )


@receiver(post_save, sender=models.Stream)
def create_notify_stream(sender, instance, created, **kwargs):
    # if instance.is_reported and instance.removed:
    #     if not created:
    #         models.Notification.objects.create(
    #             owner=instance.owner,
    #             template=3,
    #             target_id=instance.id,
    #             target_type=ContentType.objects.get_for_model(
    #                 models.Report)
    #         )
    # else:
    if created:
        models.Notification.objects.create(
            owner=instance.owner,
            template=1,
            target_id=instance.id,
            target_type=ContentType.objects.get_for_model(
                models.Stream),
            target_object=instance
        )
    elif not created:
        models.Notification.objects.create(
            owner=instance.owner,
            template=2,
            target_id=instance.id,
            target_type=ContentType.objects.get_for_model(
                models.Stream),
            target_object=instance
        )


# Need modification
@receiver(post_save, sender=models.Lobby)
def create_notify_lobby(sender, instance, created, **kwargs):
    if created:
        models.Notification.objects.create(
            owner=instance.owner,
            template=4,
            target_id=instance.id,
            target_type=ContentType.objects.get_for_model(
                models.Lobby),
            target_object=instance
        )


@receiver(post_save, sender=models.LobbyMembership)
def create_notify_membership(sender, instance, created, **kwargs):
    if int(instance.status) == 2:
        print("hello")
        if not created:
            models.Notification.objects.create(
                owner=instance.member.owner,
                template=5,
                target_id=instance.id,
                target_type=ContentType.objects.get_for_model(
                    models.LobbyMembership),
                target_object=instance
            )
    if int(instance.status) == 1:
        print("hello")
        if not created:
            models.Notification.objects.create(
                owner=instance.member.owner,
                template=6,
                target_id=instance.id,
                target_type=ContentType.objects.get_for_model(
                    models.LobbyMembership),
                target_object=instance
            )


@receiver(post_save, sender=models.Comment)
def create_notify_comment(sender, instance, created, **kwargs):
    print(instance)
    print(instance.report)
    print(instance.report.content_type)
    if instance.reported and instance.removed:
        print("inside")
        if not created:
            models.Notification.objects.create(
                owner=instance.owner,
                template=8,
                target_id=instance.id,
                target_type=ContentType.objects.get_for_model(
                    models.Report),
                target_object=instance.report
            )
    else:
        if created:
            models.Notification.objects.create(
                owner=instance.lobby.owner,
                template=7,
                target_id=instance.id,
                target_type=ContentType.objects.get_for_model(
                    models.Comment),
                target_object=instance
            )
