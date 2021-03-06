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
    list_display = ('uuid', 'shortcode',)

    readonly_fields = ('uuid', 'shortcode',)
    fieldsets = (
        ("Identifiers", {'fields': ('uuid', 'shortcode',)}),
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
