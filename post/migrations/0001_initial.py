# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0003_act'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('post_title', models.CharField(blank=True, max_length=30)),
                ('post_content', models.CharField(max_length=140)),
                ('post_thumb_url', models.URLField()),
                ('post_thumb_width', models.IntegerField()),
                ('post_thumb_height', models.IntegerField()),
                ('nsfw', models.IntegerField()),
                ('post_create_time', models.DateTimeField(auto_now=True)),
                ('act', models.ForeignKey(related_name='post_act', to='activities.Act')),
                ('user', models.ForeignKey(related_name='post_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
