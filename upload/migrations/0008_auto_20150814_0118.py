# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0007_auto_20150813_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequencymessage',
            name='date',
            field=models.CharField(max_length=7),
        ),
    ]
