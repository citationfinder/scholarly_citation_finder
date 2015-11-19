# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_for_citations', '0002_auto_20151105_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='journal',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='source_extracted',
            field=models.BooleanField(default=False),
        ),
    ]
