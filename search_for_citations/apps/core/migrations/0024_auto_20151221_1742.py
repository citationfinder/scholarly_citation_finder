# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_author_coauthors'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationReference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('context', models.TextField(null=True, blank=True)),
                ('self', models.BooleanField(default=False)),
                ('publication', models.ForeignKey(related_name='publicationreference_publication', to='core.Publication')),
                ('reference', models.ForeignKey(related_name='publicationreference_citation', to='core.Publication')),
            ],
        ),
        migrations.RemoveField(
            model_name='citation',
            name='publication',
        ),
        migrations.RemoveField(
            model_name='citation',
            name='reference',
        ),
        migrations.DeleteModel(
            name='Citation',
        ),
    ]
