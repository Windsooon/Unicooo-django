from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import MyUser
from post.models import Post
from activities.models import Act


@receiver(post_save, sender=MyUser)
def init_user(sender, **kwargs):
    user = kwargs['instance']
    cache.set("email_" + user.email, 1, timeout=None)
    cache.set("user_name_" + user.user_name, 1, timeout=None)
    cache.set("user_points_" + str(user.id), 50, timeout=None)


@receiver(post_save, sender=Post)
def init_post(sender, **kwargs):
    post = kwargs['instance']
    cache.set("post_"+str(post.id), 0, timeout=None)


@receiver(post_save, sender=Act)
def init_act(sender, **kwargs):
    act = kwargs['instance']
    cache.set("act_"+str(act.id), 0, timeout=None)
