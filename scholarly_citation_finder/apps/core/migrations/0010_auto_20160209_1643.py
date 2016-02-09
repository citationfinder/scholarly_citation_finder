# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20160128_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='conference',
            name='short_name',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
