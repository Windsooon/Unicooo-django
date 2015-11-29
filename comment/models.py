from django.db import models
from post.models import Post
from common.models import MyUser

class Comment(models.Model):
    post = models.ForeignKey("post.Post", related_name="comment_post")
    user = models.ForeignKey("common.MyUser", related_name="comment_user")
    reply_id = models.IntegerField()
    comment_content = models.CharField(max_length=30)
    comment_create_time = models.DateTimeField(auto_now=True)


