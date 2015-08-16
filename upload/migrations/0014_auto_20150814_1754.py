# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0013_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='datetime',
            field=models.DateTimeField(),
        ),
    ]
