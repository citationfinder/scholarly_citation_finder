# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_publication_arxiv_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationUrls',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'application/pdf', max_length=50, choices=[(b'application/pdf', b'PDF'), (b'text/html', b'HTML')])),
                ('url', models.URLField()),
                ('publication', models.ForeignKey(to='core.Publication')),
            ],
        ),
    ]
