# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_publication_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='source',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
