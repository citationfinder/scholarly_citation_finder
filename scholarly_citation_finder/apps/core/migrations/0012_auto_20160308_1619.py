# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-08 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20160308_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True),
        ),
    ]