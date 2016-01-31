# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0002_auto_20151127_0521'),
    ]

    operations = [
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('act_title', models.CharField(max_length=30)),
                ('act_content', models.CharField(max_length=1000)),
                ('act_thumb_url', models.CharField(max_length=400)),
                ('act_ident', models.IntegerField(unique=True)),
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
    ]
