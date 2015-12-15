# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20151208_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='coauthors',
            field=models.ManyToManyField(related_name='_coauthors_+', to='core.Author'),
        ),
    ]
