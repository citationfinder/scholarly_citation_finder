# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-09 01:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_publicationurl_extraction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationreference',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.PublicationUrl'),
        ),
    ]
