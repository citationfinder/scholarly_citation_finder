# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20160224_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(max_length=30, choices=[(b'citation/mag', b'citation/mag'), (b'evaluation/set', b'evaluation/set'), (b'evaluation/run', b'evaluation/run'), (b'harvester', b'harvester')]),
        ),
    ]
