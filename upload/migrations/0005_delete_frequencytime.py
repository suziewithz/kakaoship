# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_auto_20150813_1910'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FrequencyTime',
        ),
    ]
