# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0014_auto_20150814_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
