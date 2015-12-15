# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151105_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='citation',
            name='context',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='abstract',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='booktitle',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='citeseerx_id',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='date',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='dblp_id',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='doi',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='journal',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='pages',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publisher',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='source',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.CharField(max_length=150, blank=True),
        ),
    ]
