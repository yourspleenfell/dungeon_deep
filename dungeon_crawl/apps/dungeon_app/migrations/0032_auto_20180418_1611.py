# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-18 23:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dungeon_app', '0031_auto_20180418_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='monsters_killed',
            field=models.TextField(default='', null=True),
        ),
    ]