# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-18 11:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20160313_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorNameBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=52)),
            ],
        ),
        migrations.CreateModel(
            name='AuthorNameVariation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=20)),
                ('middle', models.CharField(blank=True, max_length=20, null=True)),
                ('last', models.CharField(max_length=50)),
                ('suffix', models.CharField(blank=True, max_length=10, null=True)),
                ('nickname', models.CharField(blank=True, max_length=20, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Author')),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.AuthorNameBlock')),
            ],
        ),
    ]
