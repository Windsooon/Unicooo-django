from django.db import models
from common.models import MyUser
from .choices import ACTTYPE, ACTLICENCE


class Act(models.Model):
    user = models.ForeignKey("common.MyUser", related_name="act_user")
    act_title = models.CharField(max_length=30)
    act_content = models.CharField(max_length=1000)
    act_thumb_url = models.CharField(max_length=400)
    act_ident = models.IntegerField(default=1000)
    act_type = models.IntegerField(choices=ACTTYPE, default=ACTTYPE[1][0])
    act_licence = models.IntegerField(choices=ACTLICENCE, default=ACTLICENCE[1][0])
    act_star = models.IntegerField(default=0)
    act_status = models.IntegerField(default=0) 
    act_url = models.CharField(max_length=255)
    act_delete = models.IntegerField(default=0)
    act_create_time = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = [
            ["user", "act_title"],
        ]
        

