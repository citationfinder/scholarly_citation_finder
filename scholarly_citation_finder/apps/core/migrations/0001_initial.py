# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Affilation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=100, null=True, blank=True)),
                ('url', models.URLField(max_length=100, null=True, blank=True)),
                ('year', models.PositiveIntegerField(max_length=4, null=True, blank=True)),
                ('conference', models.ForeignKey(to='core.Conference')),
            ],
        ),
        migrations.CreateModel(
            name='FieldOfStudy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50, null=True, blank=True)),
                ('title', models.CharField(max_length=250, null=True, blank=True)),
                ('date', models.CharField(max_length=50, null=True, blank=True)),
                ('year', models.PositiveIntegerField(max_length=4, null=True, blank=True)),
                ('booktitle', models.CharField(max_length=200, null=True, blank=True)),
                ('volume', models.CharField(max_length=20, null=True, blank=True)),
                ('number', models.CharField(max_length=20, null=True, blank=True)),
                ('pages_from', models.CharField(max_length=5, null=True, blank=True)),
                ('pages_to', models.CharField(max_length=5, null=True, blank=True)),
                ('series', models.CharField(max_length=200, null=True, blank=True)),
                ('publisher', models.CharField(max_length=150, null=True, blank=True)),
                ('isbn', models.CharField(max_length=50, null=True, blank=True)),
                ('doi', models.CharField(max_length=50, null=True, blank=True)),
                ('abstract', models.TextField(null=True, blank=True)),
                ('copyright', models.TextField(null=True, blank=True)),
                ('source_extracted', models.BooleanField(default=False)),
                ('journal', models.ForeignKey(blank=True, to='core.Journal', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublicationAuthorAffilation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('affilation', models.ForeignKey(blank=True, to='core.Affilation', null=True)),
                ('author', models.ForeignKey(to='core.Author')),
                ('publication', models.ForeignKey(to='core.Publication')),
            ],
        ),
        migrations.CreateModel(
            name='PublicationKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('fieldofstudy', models.ForeignKey(blank=True, to='core.FieldOfStudy', null=True)),
                ('publication', models.ForeignKey(to='core.Publication')),
            ],
        ),
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
        migrations.CreateModel(
            name='PublicationUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('type', models.CharField(default=b'', max_length=20, null=True, blank=True, choices=[(b'', b''), (b'application/pdf', b'PDF'), (b'text/html', b'HTML')])),
                ('publication', models.ForeignKey(to='core.Publication')),
            ],
        ),
    ]
