# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151105_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='date',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
