# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0009_auto_20150814_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='frequencytime',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
