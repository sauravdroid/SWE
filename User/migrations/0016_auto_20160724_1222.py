# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-24 12:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0015_auto_20160724_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date_sent',
            field=models.DateField(default=datetime.datetime(2016, 7, 24, 12, 22, 40, 516596, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hod',
            name='date_of_appointment',
            field=models.DateField(default=datetime.datetime(2016, 7, 24, 12, 22, 40, 513536, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='moderator',
            name='date_of_appointment',
            field=models.DateField(default=datetime.datetime(2016, 7, 24, 12, 22, 40, 515735, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='date_uploaded',
            field=models.DateField(default=datetime.datetime(2016, 7, 24, 12, 22, 40, 518509, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='papersetter',
            unique_together=set([('subject_name', 'appointment_year'), ('setter_user_name', 'appointment_year')]),
        ),
    ]
