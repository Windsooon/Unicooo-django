# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-23 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_auto_20151204_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='act_ident',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]