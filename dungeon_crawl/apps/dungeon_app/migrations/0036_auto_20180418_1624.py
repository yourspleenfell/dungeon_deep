# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-18 23:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dungeon_app', '0035_auto_20180418_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='total_monsters_killed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='char',
            name='monsters_killed',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='total_dmg_dealt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='total_dmg_taken',
            field=models.IntegerField(default=0),
        ),
    ]
