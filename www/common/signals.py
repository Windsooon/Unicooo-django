from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import MyUser


@receiver(post_save, sender=MyUser)
def init_user(sender, **kwargs):
    user = kwargs['instance']
    cache.set("email_" + user.email, 1, timeout=None)
    cache.set("user_name_" + user.user_name, 1, timeout=None)
    cache.set("user_points_" + str(user.id), 50, timeout=None)
