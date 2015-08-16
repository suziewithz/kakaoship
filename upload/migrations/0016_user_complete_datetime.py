# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0015_auto_20150814_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='complete_datetime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
