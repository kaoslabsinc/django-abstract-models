from django.contrib import admin
from django.http import HttpRequest

from abstract_models.abstracts import HasSession


class HasSessionAdminMixin(admin.ModelAdmin):
    def save_model(self, request: HttpRequest, obj: HasSession, form, change):
        if not obj.session_key:
            obj.session_key = request.session.session_key
        super(HasSessionAdminMixin, self).save_model(request, obj, form, change)
