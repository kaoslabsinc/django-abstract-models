from django.contrib import admin

"""
The classes in this file aren't meant to be used like Mixins or parent classes
Rather their fields are meant to be used like so
class SomethingAdmin(admin.ModelAdmin):
    list_display = HasNameAdmin.list_display + ('field1', 'field2')
"""


class HasNameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)


class HasAddressAdmin(admin.ModelAdmin):
    list_display = ('address',)
    search_fields = ('address__raw', 'address_formatted')
    fields = ('address',)


class HasOwnerAdmin(admin.ModelAdmin):
    list_display = ('owner',)
    search_fields = ('owner__username',)

    autocomplete_fields = ('owner',)


class ArchiveableAdmin(admin.ModelAdmin):
    list_display = ('archived',)
    list_filter = ('archived',)

    fieldsets = (
        ("Management", {'fields': ('archived',)}),
    )


class HasUUIDAdmin(admin.ModelAdmin):
    search_fields = ('uuid',)
    list_display = ('uuid',)
    list_display_shortcode = ('shortcode',)

    readonly_fields = ('uuid', 'shortcode',)
    fieldsets = (
        ("Identifiers", {'fields': ('uuid',)}),
    )
    fieldsets_shortcode = (
        ("Identifiers", {'fields': ('shortcode',)}),
    )


class HasSlugAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    fieldsets = (
        ("Identifiers", {'fields': ('slug',)}),
    )


class HasIconAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Media", {'fields': ('icon',)}),
    )


class HasCoverPhotoAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Media", {'fields': ('cover_photo',)}),
    )


class HasDescriptionAdmin(admin.ModelAdmin):
    fields = ('description',)


# HasXXXAdminMixin():
#   actions = ...


class TimeStampedModelAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    list_filter_extra = ('modified',)
    list_display = ('created',)
    list_display_extra = ('modified',)
    readonly_fields = ('created', 'modified')
    fieldsets = (
        ("Timestamps", {'fields': ('created', 'modified')}),
    )


class HasSessionAdminComponent(admin.ModelAdmin):
    search_fields = ('session_key',)
    readonly_fields = ('session_key',)
    fieldsets = (("Session Information", {'fields': ('session_key',)}),)
