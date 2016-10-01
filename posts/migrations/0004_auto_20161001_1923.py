# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-01 13:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 1, 13, 53, 35, 386315, tzinfo=utc)),
            preserve_default=False,
        ),
    ]