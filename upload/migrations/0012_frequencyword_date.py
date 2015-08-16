# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0011_auto_20150814_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='frequencyword',
            name='date',
            field=models.CharField(max_length=7, null=True),
        ),
    ]
