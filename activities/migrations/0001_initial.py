# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-07 14:42
from __future__ import unicode_literals

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
            name='Act',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_title', models.CharField(max_length=30)),
                ('act_content', models.CharField(max_length=1000)),
                ('act_thumb_url', models.CharField(max_length=400)),
                ('act_ident', models.CharField(max_length=50, unique=True)),
                ('act_type', models.IntegerField(choices=[(0, 'Personal Activities'), (1, 'Group Activities'), (2, 'Public Activities')], default=1)),
                ('act_licence', models.IntegerField(choices=[(0, 'CC BY'), (1, 'CC BY-SA'), (2, 'CC BY-NC'), (3, 'CC BY-NC-SA'), (4, 'CC BY-ND'), (5, 'CC BY-NC-ND')], default=1)),
                ('act_star', models.IntegerField(default=0)),
                ('act_status', models.IntegerField(default=0)),
                ('act_url', models.CharField(max_length=255)),
                ('act_delete', models.IntegerField(default=0)),
                ('act_create_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='act_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterIndexTogether(
            name='act',
            index_together=set([('user', 'act_title')]),
        ),
    ]
