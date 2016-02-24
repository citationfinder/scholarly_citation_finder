# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djcelery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=30, choices=[(b'citation/mag', b'citation/mag')])),
                ('taskmeta', models.ForeignKey(to='djcelery.TaskMeta')),
            ],
        ),
    ]
