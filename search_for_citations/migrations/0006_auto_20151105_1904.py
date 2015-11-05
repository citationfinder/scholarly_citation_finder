# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_for_citations', '0005_auto_20151105_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='booktitle',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='pages',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='publication',
            name='abstract',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='publication',
            name='citeseerx_id',
            field=models.CharField(default=None, max_length=150),
        ),
        migrations.AlterField(
            model_name='publication',
            name='date',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='publication',
            name='dblp_id',
            field=models.CharField(default=None, max_length=150),
        ),
        migrations.AlterField(
            model_name='publication',
            name='doi',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='publication',
            name='journal',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publisher',
            field=models.CharField(default=None, max_length=150),
        ),
        migrations.AlterField(
            model_name='publication',
            name='source',
            field=models.URLField(default=None),
        ),
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.CharField(default=None, max_length=150),
        ),
    ]
