# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_act'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='act_licence',
            field=models.IntegerField(choices=[(0, 'CC BY'), (1, 'CC BY-SA'), (2, 'CC BY-ND'), (3, 'CC BY-NC'), (4, 'CC BY-NC-SA'), (5, 'CC BY-NC-ND')], default=0),
        ),
        migrations.AlterField(
            model_name='act',
            name='act_type',
            field=models.IntegerField(choices=[(0, 'Personal Activities'), (1, 'Group Activities'), (2, 'Public Activities')], default=0),
        ),
        migrations.AlterField(
            model_name='act',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='act_user'),
        ),
    ]
