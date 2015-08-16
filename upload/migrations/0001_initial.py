# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FrequencyMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=20)),
                ('date', models.DateTimeField(verbose_name=b'date published')),
                ('count', models.IntegerField(default=0)),
                ('byte', models.IntegerField(default=0)),
            ],
        ),
    ]
