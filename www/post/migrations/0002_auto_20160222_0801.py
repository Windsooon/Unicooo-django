# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-22 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_thumb_url',
            field=models.CharField(max_length=255),
        ),
    ]
