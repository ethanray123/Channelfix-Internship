# Generated by Django 2.0.5 on 2018-05-17 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('removed', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lobby', to='stream.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moderator', to='stream.Lobby')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='moderator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('URL', models.CharField(max_length=200)),
                ('removed', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('tag', models.IntegerField(choices=[(0, 'Guest'), (1, 'Sponsor'), (2, 'Player'), (3, 'Main')], default=0)),
                ('lobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='streams', to='stream.Lobby')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stream', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
