# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-08 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30)),
                ('starttime', models.DateTimeField(auto_now_add=True)),
                ('taskmeta_id', models.CharField(max_length=100)),
            ],
        ),
    ]
