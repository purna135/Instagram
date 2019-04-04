# Generated by Django 2.2 on 2019-04-04 18:19

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='', max_length=20)),
                ('follower', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baseurl', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
                ('owner', models.CharField(max_length=20)),
                ('likes', models.IntegerField()),
                ('caption', models.CharField(default='', max_length=140)),
                ('tags', models.IntegerField(default=0)),
                ('main_colour', models.CharField(default='', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='PhotoLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postid', models.IntegerField()),
                ('liker', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PhotoTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photoid', models.IntegerField()),
                ('coords', models.CharField(max_length=20)),
                ('tagged_user', models.CharField(default='', max_length=20)),
                ('tagged_by', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profilepic', models.CharField(default='', max_length=255)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]