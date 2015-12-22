# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20151221_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('publication', models.ForeignKey(to='core.Publication')),
            ],
        ),
    ]
