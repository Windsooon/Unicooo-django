# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-05-03 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20170402_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='act_intro',
            field=models.TextField(blank=True, null=True),
        ),
    ]
