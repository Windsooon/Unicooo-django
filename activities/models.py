from django.db import models
from common.models import MyUser

class Act(models.Model):
    user = models.ForeignKey("common.MyUser")
    act_title = models.CharField(max_length=30)
    act_content = models.CharField(max_length=1000)
    act_thumb_url = models.CharField(max_length=400)
    act_ident = models.IntegerField(unique=True)
    act_type = models.IntegerField()
    act_licence = models.IntegerField()
    act_star = models.IntegerField(default=0)
    act_status = models.IntegerField(default=0) 
    act_url = models.URLField()
    act_delete = models.IntegerField(default=0)
    act_create_time = models.DateTimeField(auto_now=True)

