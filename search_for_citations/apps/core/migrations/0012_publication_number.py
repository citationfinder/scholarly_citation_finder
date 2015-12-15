# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_publication_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='number',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
