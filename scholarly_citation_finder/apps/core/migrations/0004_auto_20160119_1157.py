# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_publication_conference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferenceinstance',
            name='conference',
            field=models.ForeignKey(blank=True, to='core.Conference', null=True),
        ),
    ]
