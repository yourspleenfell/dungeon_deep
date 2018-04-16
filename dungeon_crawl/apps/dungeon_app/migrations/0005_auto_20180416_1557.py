# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-16 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dungeon_app', '0004_remove_mon_defense'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mon',
            old_name='vitality',
            new_name='current_vitality',
        ),
        migrations.AddField(
            model_name='mon',
            name='max_vitality',
            field=models.IntegerField(default=110),
            preserve_default=False,
        ),
    ]
