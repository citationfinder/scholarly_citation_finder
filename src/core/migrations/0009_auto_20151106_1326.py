# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20151106_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='volume',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
