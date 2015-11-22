# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_publication_extractor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citation',
            name='citation',
        ),
        migrations.AlterField(
            model_name='citation',
            name='publication',
            field=models.ForeignKey(to='core.Publication'),
        ),
    ]
