from django.db import models
from activities.choices import POSTMIME


class Post(models.Model):
    user = models.ForeignKey("common.MyUser", related_name="post_user")
    act = models.ForeignKey("activities.Act", related_name="post_act")
    post_title = models.CharField(max_length=30, blank=True)
    post_content = models.CharField(max_length=140)
    post_url = models.URLField(blank=True)
    post_thumb_url = models.CharField(max_length=512)
    post_thumb_width = models.FloatField()
    post_thumb_height = models.FloatField()
    post_mime_types = models.IntegerField(
            choices=POSTMIME,
            default=POSTMIME[0][0])
    nsfw = models.IntegerField()
    post_create_time = models.DateTimeField(auto_now=True)
    post_update_time = models.DateTimeField(auto_now_add=True)
