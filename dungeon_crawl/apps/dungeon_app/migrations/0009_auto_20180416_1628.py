# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-16 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dungeon_app', '0008_auto_20180416_1626'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='gold',
            new_name='attack_max',
        ),
        migrations.AddField(
            model_name='item',
            name='attack_min',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='cost',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='defense',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='vitality',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
