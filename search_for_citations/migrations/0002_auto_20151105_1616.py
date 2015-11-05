# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_for_citations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='doi',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='publisher',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='source_extracted',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='volume',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publication',
            name='citeseerx_id',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='dblp_id',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='source',
            field=models.URLField(null=True),
        ),
    ]
