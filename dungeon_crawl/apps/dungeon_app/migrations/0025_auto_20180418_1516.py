# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-18 22:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dungeon_app', '0024_auto_20180418_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='active_char',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='active_user', to='dungeon_app.Char'),
        ),
    ]