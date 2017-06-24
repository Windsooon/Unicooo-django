from django.db import models


class Comment(models.Model):
    post = models.ForeignKey(
        "post.Post", related_name="comment_post", on_delete=models.CASCADE)
    user = models.ForeignKey(
        "common.MyUser", related_name="comment_user", on_delete=models.CASCADE)
    reply_id = models.IntegerField()
    comment_content = models.CharField(max_length=140)
    comment_create_time = models.DateTimeField(auto_now=True)
    comment_update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_create_time']

    def __str__(self):
        return self.comment_content
