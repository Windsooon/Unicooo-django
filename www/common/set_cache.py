from common.models import MyUser
from post.models import Post
from act.models import Act
from django.core.cache import cache

user_list = MyUser.objects.all()
post_list = Post.objects.all()
act_list = Act.objects.all()

for user in user_list:
    cache.set("email_" + user.email, 1, timeout=None)
    cache.set("user_name_" + user.user_name, 1, timeout=None)
    cache.set("user_points_" + str(user.id), 50, timeout=None)

for act in act_list:
    cache.set("act_"+str(act.id), 0, timeout=None)

for post in post_list:
    cache.set("post_"+str(post.id), 0, timeout=None)
