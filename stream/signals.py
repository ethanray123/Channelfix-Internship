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
            target_id=instance.id,
            target_type=ContentType.objects.get_for_model(models.Subscription)
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
                models.Stream)
        )
    elif not created:
        models.Notification.objects.create(
            owner=instance.owner,
            template=2,
            target_id=instance.id,
            target_type=ContentType.objects.get_for_model(
                models.Stream)
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
                models.Lobby)
        )


@receiver(post_save, sender=models.LobbyMembership)
def create_notify_membership(sender, instance, created, **kwargs):
    if instance.status == 2:
        if not created:
            models.Notification.objects.create(
                owner=instance.member.owner,
                template=5,
                target_id=instance.id,
                target_type=ContentType.objects.get_for_model(
                    models.LobbyMembership)
            )
    if instance.status == 1:
        if not created:
            models.Notification.objects.create(
                owner=instance.member.owner,
                template=6,
                target_id=instance.id,
                target_type=ContentType.objects.get_for_model(
                    models.LobbyMembership)
            )


@receiver(post_save, sender=models.Comment)
def create_notify_comment(sender, instance, created, **kwargs):
    if instance.is_reported and instance.removed:
        if not created:
            models.Notification.objects.create(
                owner=instance.owner,
                template=8,
                target_id=instance.id,
                target_type=ContentType.objects.get_for_model(
                    models.Report)
            )
    else:
        if not created:
            models.Notification.objects.create(
                owner=instance.lobby.owner,
                template=7,
                target_id=instance.id,
                target_type=ContentType.objects.get_for_model(
                    models.Comment)
            )
