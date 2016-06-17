# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('short_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hash',
            name='bookmark',
        ),
        migrations.AddField(
            model_name='bookmark',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='hash_id',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.DeleteModel(
            name='Hash',
        ),
    ]
