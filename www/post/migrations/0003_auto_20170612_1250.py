# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-06-12 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20170603_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_url',
            field=models.URLField(blank=True),
        ),
    ]
