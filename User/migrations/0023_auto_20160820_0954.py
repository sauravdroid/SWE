# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-20 09:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0022_auto_20160727_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date_sent',
            field=models.DateField(default=datetime.datetime(2016, 8, 20, 9, 54, 45, 486718, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hod',
            name='date_of_appointment',
            field=models.DateField(default=datetime.datetime(2016, 8, 20, 9, 54, 45, 483736, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='moderator',
            name='date_of_appointment',
            field=models.DateField(default=datetime.datetime(2016, 8, 20, 9, 54, 45, 485945, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='date_uploaded',
            field=models.DateField(default=datetime.datetime(2016, 8, 20, 9, 54, 45, 488435, tzinfo=utc)),
        ),
    ]
