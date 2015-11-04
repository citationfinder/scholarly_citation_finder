# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Citation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('context', models.TextField()),
                ('self', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('abstract', models.TextField()),
                ('journal', models.CharField(max_length=150)),
                ('source', models.URLField()),
                ('citeseerx_id', models.CharField(max_length=150)),
                ('dblp_id', models.CharField(max_length=150)),
                ('authors', models.ManyToManyField(to='search_for_citations.Author')),
            ],
        ),
        migrations.AddField(
            model_name='citation',
            name='citation',
            field=models.OneToOneField(related_name='citation_citation', to='search_for_citations.Publication'),
        ),
        migrations.AddField(
            model_name='citation',
            name='publication',
            field=models.OneToOneField(related_name='citation_publication', to='search_for_citations.Publication'),
        ),
    ]
