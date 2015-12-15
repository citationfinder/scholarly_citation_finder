# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_publicationurls'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publication',
            old_name='pages',
            new_name='pages_from',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='source',
        ),
        migrations.AddField(
            model_name='publication',
            name='isbn',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='pages_to',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='series',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
