from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_content', 'post', 'comment_create_time')
    search_fields = ('comment_content',)

admin.site.register(Comment, CommentAdmin)
