# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-01 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20180101_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='img',
            field=models.ImageField(default='image/default.png', upload_to='user_img/%Y/%m', verbose_name='头像'),
        ),
    ]