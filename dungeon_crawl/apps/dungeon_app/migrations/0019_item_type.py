# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-17 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dungeon_app', '0018_mon_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
