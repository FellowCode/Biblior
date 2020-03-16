from django.contrib import admin

from Publications.models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    pass