# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-24 12:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0014_auto_20160724_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date_sent',
            field=models.DateField(default=datetime.datetime(2016, 7, 24, 12, 21, 59, 811733, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hod',
            name='date_of_appointment',
            field=models.DateField(default=datetime.datetime(2016, 7, 24, 12, 21, 59, 808754, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='moderator',
            name='date_of_appointment',
            field=models.DateField(default=datetime.datetime(2016, 7, 24, 12, 21, 59, 810925, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='date_uploaded',
            field=models.DateField(default=datetime.datetime(2016, 7, 24, 12, 21, 59, 813626, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='papersetter',
            unique_together=set([('setter_user_name', 'appointment_year')]),
        ),
    ]