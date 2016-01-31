from django.db import models
from common.models import MyUser
from activities.models import Act


class Post(models.Model):
    user = models.ForeignKey("common.MyUser", related_name="post_user")
    act = models.ForeignKey("activities.Act", related_name="post_act")
    post_title = models.CharField(max_length=30, blank=True)
    post_content = models.CharField(max_length=140)
    post_thumb_url = models.URLField()
    post_thumb_width = models.IntegerField()
    post_thumb_height = models.IntegerField()
    nsfw = models.IntegerField()
    post_create_time = models.DateTimeField(auto_now=True)

