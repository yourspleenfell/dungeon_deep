# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-17 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dungeon_app', '0012_auto_20180417_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='monsters_killed',
            field=models.ManyToManyField(blank=True, default='', related_name='slayers', to='dungeon_app.Mon'),
        ),
        migrations.AlterField(
            model_name='user',
            name='total_dmg_dealt',
            field=models.IntegerField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='total_dmg_taken',
            field=models.IntegerField(blank=True, default=''),
        ),
    ]
