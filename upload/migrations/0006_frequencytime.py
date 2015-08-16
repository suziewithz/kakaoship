# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_delete_frequencytime'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrequencyTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(max_length=30)),
                ('data', models.CharField(max_length=255)),
            ],
        ),
    ]
