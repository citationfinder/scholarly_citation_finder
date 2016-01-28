# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20160128_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationurl',
            name='type',
            field=models.CharField(default=b'', max_length=30, null=True, blank=True, choices=[(b'', b''), (b'application/pdf', b'PDF'), (b'text/html', b'HTML')]),
        ),
    ]
