from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from Publications.models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    def user_email(self, obj):
        url = reverse('admin:Accounts_user_change', args=[obj.user.id])
        return format_html("<a href='{}'>{}</a>", url, obj.user.email)

    user_email.admin_order_field = 'user__email'

    list_display = ['user_email', 'title']

    list_display_links = ['title']