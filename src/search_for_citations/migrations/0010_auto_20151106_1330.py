# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_for_citations', '0009_auto_20151106_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='citation',
            name='context',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='abstract',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='booktitle',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='citeseerx_id',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='date',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='dblp_id',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='doi',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='journal',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='pages',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publisher',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='source',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='volume',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
