# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-18 22:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dungeon_app', '0026_auto_20180418_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='dead_chars',
        ),
        migrations.AddField(
            model_name='user',
            name='characters',
            field=models.ManyToManyField(null=True, related_name='created_by', to='dungeon_app.Char'),
        ),
    ]
