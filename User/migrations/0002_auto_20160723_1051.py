# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-23 10:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date_sent',
            field=models.DateField(default=datetime.datetime(2016, 7, 23, 10, 51, 7, 801338, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hod',
            name='date_of_appointment',
            field=models.DateField(default=datetime.datetime(2016, 7, 23, 10, 51, 7, 798334, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='moderator',
            name='date_of_appointment',
            field=models.DateField(default=datetime.datetime(2016, 7, 23, 10, 51, 7, 800548, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='date_uploaded',
            field=models.DateField(default=datetime.datetime(2016, 7, 23, 10, 51, 7, 803260, tzinfo=utc)),
        ),
    ]
