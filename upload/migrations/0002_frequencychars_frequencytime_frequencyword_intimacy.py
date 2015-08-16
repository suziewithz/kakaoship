# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrequencyChars',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=20)),
                ('count_char_1', models.IntegerField(default=0)),
                ('count_char_2', models.IntegerField(default=0)),
                ('count_char_3', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FrequencyTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(max_length=30)),
                ('date', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FrequencyWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(max_length=30)),
                ('word', models.CharField(max_length=20)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Intimacy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=20)),
                ('target', models.CharField(max_length=20)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
