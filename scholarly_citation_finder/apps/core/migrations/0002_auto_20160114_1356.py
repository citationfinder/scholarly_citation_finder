# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferenceinstance',
            name='year',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='year',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
