# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 11:07
from __future__ import unicode_literals

import ditto.core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, help_text='The time this item was created in the database.')),
                ('time_modified', models.DateTimeField(auto_now=True, help_text='The time this item was last saved to the database.')),
                ('username', models.CharField(help_text="eg, 'rj'", max_length=30, unique=True)),
                ('realname', models.CharField(help_text="eg, 'Richard Jones'", max_length=30)),
                ('api_key', models.CharField(blank=True, max_length=255, verbose_name='API Key')),
                ('is_active', models.BooleanField(default=True, help_text="If false, new scrobbles won't be fetched.")),
            ],
            options={
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, help_text='The time this item was created in the database.')),
                ('time_modified', models.DateTimeField(auto_now=True, help_text='The time this item was last saved to the database.')),
                ('name', models.TextField()),
                ('slug', models.TextField(db_index=True)),
                ('mbid', models.CharField(blank=True, help_text='MusicBrainz Identifier', max_length=36, verbose_name='MBID')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, help_text='The time this item was created in the database.')),
                ('time_modified', models.DateTimeField(auto_now=True, help_text='The time this item was last saved to the database.')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.TextField(unique=True)),
                ('mbid', models.CharField(blank=True, help_text='MusicBrainz Identifier', max_length=36, verbose_name='MBID')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Scrobble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, help_text='The time this item was created in the database.')),
                ('time_modified', models.DateTimeField(auto_now=True, help_text='The time this item was last saved to the database.')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('permalink', models.URLField(blank=True, help_text="URL of the item on the service's website.")),
                ('summary', models.CharField(blank=True, help_text="eg, Initial text of a blog post, start of the description of a photo, all of a Tweet's text, etc. No HTML.", max_length=255)),
                ('is_private', models.BooleanField(default=False, help_text='If true, this item will not be shown on public-facing pages.')),
                ('fetch_time', models.DateTimeField(blank=True, help_text="The time the item's data was last fetched.", null=True)),
                ('post_time', models.DateTimeField(blank=True, help_text='The time the item was originally posted/created on its service.', null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('raw', models.TextField(blank=True, help_text='eg, the raw JSON from the API.')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lastfm.Account')),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scrobbles', to='lastfm.Album')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scrobbles', to='lastfm.Artist')),
            ],
            options={
                'ordering': ['-post_time'],
            },
            bases=(ditto.core.models.DiffModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, help_text='The time this item was created in the database.')),
                ('time_modified', models.DateTimeField(auto_now=True, help_text='The time this item was last saved to the database.')),
                ('name', models.TextField()),
                ('slug', models.TextField(db_index=True)),
                ('mbid', models.CharField(blank=True, help_text='MusicBrainz Identifier', max_length=36, verbose_name='MBID')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='lastfm.Artist')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='scrobble',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scrobbles', to='lastfm.Track'),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='lastfm.Artist'),
        ),
    ]