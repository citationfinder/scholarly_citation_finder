# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 24, 13, 26, 51, 421357), auto_now_add=True),
            preserve_default=False,
        ),
    ]
