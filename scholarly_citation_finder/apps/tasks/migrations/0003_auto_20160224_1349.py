# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_starttime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='taskmeta',
        ),
        migrations.AddField(
            model_name='task',
            name='taskmeta_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
