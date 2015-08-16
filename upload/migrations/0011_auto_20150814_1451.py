# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0010_frequencytime_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='frequencytime',
            old_name='weekday',
            new_name='week',
        ),
    ]
