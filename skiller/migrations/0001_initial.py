# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-20 13:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Confirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='confirmations_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('serial', models.AutoField(primary_key=True, serialize=False)),
                ('codename', models.CharField(help_text='codename for the skill', max_length=20, unique=True)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='confirmation',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skiller.Skill'),
        ),
        migrations.AddField(
            model_name='confirmation',
            name='to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='confirmations_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='confirmation',
            unique_together=set([('to', 'skill', 'by')]),
        ),
    ]
