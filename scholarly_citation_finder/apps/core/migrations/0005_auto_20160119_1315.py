# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160119_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationreference',
            name='self',
            field=models.NullBooleanField(default=False),
        ),
    ]
