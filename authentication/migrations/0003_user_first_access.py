# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-07 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20180605_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_access',
            field=models.BooleanField(default=True),
        ),
    ]
