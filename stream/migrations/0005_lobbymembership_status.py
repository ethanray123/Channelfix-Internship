# Generated by Django 2.0 on 2018-05-31 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0004_lobby_lobby_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobbymembership',
            name='status',
            field=models.IntegerField(choices=[(0, 'PENDING'), (1, 'REJECTED'), (2, 'ACCEPTED')], default=0),
        ),
    ]
