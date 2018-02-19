# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-18 23:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friendship', '0005_auto_20180218_2307'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('to', 'by'), ('by', 'to')]),
        ),
    ]
