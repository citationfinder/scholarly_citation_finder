# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20160119_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='source_extracted',
            field=models.NullBooleanField(default=False),
        ),
    ]
