from django.contrib import admin

from .models import Act


class ActAdmin(admin.ModelAdmin):
    list_display = ('act_title', 'act_content', 'act_type', 'act_create_time')
    search_fields = ('act_title')

admin.site.register(Act, ActAdmin)
