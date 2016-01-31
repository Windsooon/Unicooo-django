# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('email', models.EmailField(verbose_name='Email Address', max_length=255, unique=True)),
                ('user_name', models.CharField(max_length=30, unique=True)),
                ('user_avatar', models.URLField()),
                ('user_gender', models.IntegerField(default=0)),
                ('user_point', models.IntegerField(default=0)),
                ('user_details', models.CharField(max_length=80)),
                ('user_register_time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'common_user',
            },
        ),
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_title', models.CharField(max_length=30)),
                ('act_content', models.CharField(max_length=400)),
                ('act_thumb_url', models.CharField(max_length=400)),
                ('act_ident', models.IntegerField()),
                ('act_type', models.IntegerField()),
                ('act_licence', models.IntegerField()),
                ('act_star', models.IntegerField(default=0)),
                ('act_status', models.IntegerField(default=0)),
                ('act_url', models.URLField()),
                ('act_delete', models.IntegerField(default=0)),
                ('act_create_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_id', models.IntegerField()),
                ('comment_content', models.CharField(max_length=30)),
                ('comment_create_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=30)),
                ('post_content', models.CharField(max_length=140)),
                ('post_thumb_url', models.URLField()),
                ('post_thumb_width', models.IntegerField()),
                ('post_thumb_height', models.IntegerField()),
                ('nsfw', models.IntegerField()),
                ('post_create_time', models.DateTimeField(auto_now=True)),
                ('act', models.ForeignKey(to='common.Act')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='common.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
