# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0003_auto_20150813_1526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='frequencytime',
            old_name='date',
            new_name='data',
        ),
    ]
