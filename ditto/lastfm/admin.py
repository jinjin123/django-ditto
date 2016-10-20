from django.contrib import admin
from django.utils.html import format_html

from .models import Account, Album, Artist, Scrobble, Track


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'realname', 'is_active', 'time_created',)
    search_fields = ('name', 'artist', 'mbid',)

    fieldsets = (
        (None, {
            'fields': ('username', 'realname', 'api_key', 'is_active', )
        }),
        ('Data', {
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'mbid', 'time_created',)
    search_fields = ('name', 'mbid',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'mbid',)
        }),
        ('Data', {
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'mbid', 'time_created',)
    search_fields = ('name', 'artist', 'mbid',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'artist', 'mbid',)
        }),
        ('Data', {
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'mbid', 'time_created',)
    search_fields = ('name', 'artist',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'artist', 'mbid',)
        }),
        ('Data', {
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)


@admin.register(Scrobble)
class ScrobbleAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_time',)
    list_filter = ('post_time', )
    search_fields = ('title', 'track__name',)

    fieldsets = (
        (None, {
            'fields': ('account', 'artist', 'track', 'album', 'post_time',)
        }),
        ('Data', {
            'fields': ('raw', 'fetch_time', 'time_created', 'time_modified',)
        }),
    )

    raw_id_fields = ('artist', 'track', 'album',)
    readonly_fields = ('raw', 'fetch_time', 'time_created', 'time_modified',)
