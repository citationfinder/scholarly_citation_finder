# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_for_citations', '0013_auto_20151108_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='volume',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
