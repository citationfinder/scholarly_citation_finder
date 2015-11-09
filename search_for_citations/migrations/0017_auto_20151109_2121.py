# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_for_citations', '0016_auto_20151109_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='citation',
            name='reference',
            field=models.ForeignKey(related_name='citation_citation', default=None, to='search_for_citations.Publication'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='citation',
            name='publication',
            field=models.ForeignKey(related_name='citation_publication', to='search_for_citations.Publication'),
        ),
    ]
