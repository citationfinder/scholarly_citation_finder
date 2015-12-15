# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20151208_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='copyright',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
