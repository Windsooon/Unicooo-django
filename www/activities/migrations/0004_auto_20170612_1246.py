# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-06-12 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_act_act_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='act_content',
            field=models.CharField(max_length=200),
        ),
    ]