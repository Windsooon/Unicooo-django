# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('act_title', models.CharField(max_length=30)),
                ('act_content', models.CharField(max_length=400)),
                ('act_thumb_url', models.CharField(max_length=400)),
                ('act_ident', models.IntegerField(unique=True)),
                ('act_type', models.IntegerField()),
                ('act_licence', models.IntegerField()),
                ('act_star', models.IntegerField(default=0)),
                ('act_status', models.IntegerField(default=0)),
                ('act_url', models.URLField()),
                ('act_delete', models.IntegerField(default=0)),
                ('act_create_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='act_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
