# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-03 23:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_learntest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='LearnTest',
        ),
    ]
