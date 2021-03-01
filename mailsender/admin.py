from django.contrib import admin

from .models import Mail


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    readonly_fields = ['dispatch_time', 'timeout']
