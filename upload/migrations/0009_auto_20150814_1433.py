# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0008_auto_20150814_0118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='frequencytime',
            name='data',
        ),
        migrations.AddField(
            model_name='frequencytime',
            name='hour',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='frequencytime',
            name='weekday',
            field=models.IntegerField(default=0),
        ),
    ]
