# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_for_citations', '0010_auto_20151106_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='type',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
