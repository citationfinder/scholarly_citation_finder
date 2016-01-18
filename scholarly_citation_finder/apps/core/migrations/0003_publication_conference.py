# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160114_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='conference',
            field=models.ForeignKey(blank=True, to='core.Conference', null=True),
        ),
    ]
