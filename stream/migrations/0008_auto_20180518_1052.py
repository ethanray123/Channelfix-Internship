# Generated by Django 2.0.5 on 2018-05-18 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0007_auto_20180518_1044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lobby_membership',
            old_name='member',
            new_name='owner',
        ),
    ]
