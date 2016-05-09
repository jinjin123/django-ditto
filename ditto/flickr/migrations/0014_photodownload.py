# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-09 16:54
from __future__ import unicode_literals

import ditto.flickr.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flickr', '0013_photoset_photos_raw'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoDownload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, help_text='The time this item was created in the database.')),
                ('time_modified', models.DateTimeField(auto_now=True, help_text='The time this item was last saved to the database.')),
                ('image_file', models.FileField(blank=True, null=True, upload_to=ditto.flickr.models.PhotoDownload.upload_path)),
                ('size', models.CharField(choices=[('original', 'Original'), ('large', 'Large'), ('square', 'Square'), ('small_320', 'Small 320'), ('small', 'Small'), ('medium_640', 'Medium 640'), ('medium_800', 'Medium 800'), ('large_1600', 'Large 1600'), ('thumbnail', 'Thumbnail'), ('large_square', 'Large square'), ('medium', 'Medium'), ('large_2048', 'Large 2048')], max_length=11)),
                ('photo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='flickr.Photo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
