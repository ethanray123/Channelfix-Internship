# Generated by Django 2.0.5 on 2018-05-25 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='stream/static/images/default_avatar.png', null=True, upload_to='stream/static/images'),
        ),
    ]
