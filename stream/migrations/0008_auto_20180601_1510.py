# Generated by Django 2.0.5 on 2018-06-01 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0007_merge_20180601_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='template',
            field=models.IntegerField(choices=[(0, '{target.owner.username} has subscribed to you'), (1, '{target.owner.username} has started a stream:         {target.title} in {target.lobby.name}'), (2, 'Your stream has been updated as {target.tag}'), (3, 'Your stream has been removed due to {target.reason}'), (4, '{target.owner.username} has created a lobby: {target.name}'), (5, 'You have been accepted as a member in the lobby:         {target.lobby.name}'), (6, 'You have been rejected as a member in the lobby:         {target.lobby.name}'), (7, '{target.owner.username} has commented in lobby: {target.lobby.name}'), (8, 'Your comment has been removed due to {target.reason}')]),
        ),
    ]