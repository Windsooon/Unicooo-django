# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-06-19 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_remove_myuser_user_name_vali'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='user_details',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
