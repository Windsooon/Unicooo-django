from django.contrib import admin
from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'user_name', 'user_details', 'user_register_time')
    search_fields = ('email', 'user_name')

admin.site.register(MyUser, MyUserAdmin)
