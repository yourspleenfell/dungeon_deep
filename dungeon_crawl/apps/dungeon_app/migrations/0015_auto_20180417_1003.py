# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-17 17:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dungeon_app', '0014_auto_20180417_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='active_char',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, related_name='active_user', to='dungeon_app.Char'),
        ),
    ]