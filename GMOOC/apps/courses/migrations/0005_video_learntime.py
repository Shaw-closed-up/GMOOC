# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-04 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_video_videourl'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='LearnTime',
            field=models.IntegerField(default=0, verbose_name='学习时长'),
        ),
    ]