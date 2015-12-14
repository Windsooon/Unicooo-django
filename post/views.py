from django.shortcuts import render
from django.db.models import Max
from post.models import Post
from django.db import connection
from random import randint

CHOISES = {
    1: [" ", "挺喜欢一个男生的，平时碰面聊聊天还有聊微信都聊得很开心，但是就没有什么进展了，不是一个学院也不是一个社团话题有点少，应该怎样暗示一下他好呢？", "http://7xokch.com1.z0.glb.clouddn.com/uni_post_17.jpg", 1, 1, 1, "2014-01-01 00:00:00+08", 1, 22],         
    2: [" ", "我想问下，如果我想在图书馆找一本书，要怎样才能知道它的检索号啊？不想找遍整个图书馆那么累～跪求指教！", "http://7xokch.com1.z0.glb.clouddn.com/uni_post_11.jpg", 1, 1, 1, "2014-01-01 00:00:00+08", 2, 22],
    3: [" ", "国家励志奖学金过了初审就是申报成功的意思吗？", "http://7xokch.com1.z0.glb.clouddn.com/uni_post_18.jpg", 1, 1, 1, "2014-01-01 00:00:00+08", 3, 22],
    4: [" ", "水表是坏的，他们说我们破坏水表，要交400元，还给了一张单据。问题是，那个热水表本来就是坏的，是他们给我宿舍装的一个坏水表。我该找谁去投诉啊？", "http://7xokch.com1.z0.glb.clouddn.com/uni_post_12.jpg", 1, 1, 1, "2014-01-01 00:00:00+08", 4, 22],
}

def create_post(request):
    number = request.GET.get("number", None)
    cursor = connection.cursor()
    for i in range(int(number)):
        post_max_id = Post.objects.all().aggregate(Max("id"))["id__max"] + 1
        post_randint = randint(1, 4)
        post_choice = CHOISES[post_randint]
        print (post_choice)
        post_choice.insert(0, post_max_id)
        cursor.execute("INSERT INTO post_post VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",post_choice)

