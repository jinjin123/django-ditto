# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-15 09:11
from __future__ import unicode_literals

import ditto.twitter.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0044_auto_20160613_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='original_image_file',
            field=models.ImageField(blank=True, default='', upload_to=ditto.twitter.models.Media.upload_path),
        ),
    ]