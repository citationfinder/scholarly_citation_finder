# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 11:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('harvester', '0003_auto_20160310_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='harvester',
            name='oai_identifier',
        ),
    ]