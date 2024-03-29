# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-03-01 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address')),
                ('user_name', models.CharField(max_length=30, unique=True)),
                ('user_avatar', models.CharField(blank=True, max_length=255)),
                ('user_gender', models.IntegerField(choices=[(0, 'SECRET'), (1, 'MALE'), (2, 'FEMALE')], default=0)),
                ('user_details', models.CharField(max_length=80)),
                ('user_register_time', models.DateTimeField(auto_now=True)),
                ('user_validated', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'common_user',
            },
        ),
    ]
