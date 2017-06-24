from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'post_content', 'user', 'post_create_time')
    search_fields = ('post_title',)

admin.site.register(Post, PostAdmin)
