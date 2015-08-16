# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0006_frequencytime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequencychars',
            name='uid',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='frequencymessage',
            name='uid',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='frequencytime',
            name='uid',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='frequencyword',
            name='uid',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='intimacy',
            name='uid',
            field=models.CharField(max_length=40),
        ),
    ]
