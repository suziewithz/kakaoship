# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_frequencychars_frequencytime_frequencyword_intimacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequencymessage',
            name='date',
            field=models.DateField(verbose_name=b'date published'),
        ),
    ]
