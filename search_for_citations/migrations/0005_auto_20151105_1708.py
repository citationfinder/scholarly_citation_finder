# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_for_citations', '0004_auto_20151105_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='abstract',
            field=models.TextField(null=True),
        ),
    ]
