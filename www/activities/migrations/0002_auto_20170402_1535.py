# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-04-02 15:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='act',
            unique_together=set([('user', 'act_title')]),
        ),
    ]
