# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_publication_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='number',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
