# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('reply_id', models.IntegerField()),
                ('comment_content', models.CharField(max_length=30)),
                ('comment_create_time', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(related_name='comment_post', to='post.Post')),
                ('user', models.ForeignKey(related_name='comment_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
