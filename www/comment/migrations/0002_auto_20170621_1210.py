# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-06-21 12:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-comment_create_time']},
        ),
    ]
