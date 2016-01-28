# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20160120_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='source',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
