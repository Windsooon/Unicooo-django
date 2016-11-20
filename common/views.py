# -*- coding: utf-8 -*-
import time
import hashlib

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from .form import UserCreateForm, UserLoginForm, UserChangeForm
from activities.models import Act
from common.models import MyUser

# redis
from django.core.cache import cache
from django_redis import get_redis_connection

# qiniu
from qiniu import Auth
from .qiniuSettings import accessKey, secretKey, bucket
from common.qiniuSettings import httpsUrl


def dictfetchall(cursor):
    """trans tuple to dict"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def anonymous_required(view_function, redirect_to=None):
    return AnonymousRequired(view_function, redirect_to)


class AnonymousRequired(object):
    def __init__(self, view_function, redirect_to):
        if redirect_to is None:
            from django.conf import settings
            redirect_to = settings.LOGIN_REDIRECT_URL
        self.view_function = view_function
        self.redirect_to = redirect_to

    def __call__(self, request, *args, **kwargs):
        if request.user is not None and request.user.is_authenticated():
            return HttpResponseRedirect(self.redirect_to)
        return self.view_function(request, *args, **kwargs)


def public_activities(request):
    render(request, "public_activities.html")


def front_page(request):
    act_list = Act.objects.filter(act_type=2).order_by("-act_create_time")[:9]
    imageStyle = "-actCoverSmall"
    # user_points = cache.get("user_points_" + str(request.user.id))
    return render(
            request, "common/frontpage.html",
            {"act_list": act_list,
             "httpsUrl": httpsUrl,
             "imageStyle": imageStyle})


@anonymous_required
def sign_up(request):
    if request.method == "GET":
        form = UserCreateForm()
        return render(request, "common/signup.html", {"form": form})
    else:
        return render(request, "error.html", {"error": "Method not accepted."})


@anonymous_required
def login_in(request):
    if request.method == "GET":
        form = UserLoginForm()
        return render(request, "common/login.html", {"form": form})
    elif request.method == "POST":
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return render(
                        request, "error.html",
                        {
                            "error": "Method not accepted."
                        }
                    )
        else:
            return HttpResponse("Email or password incorrect.", status=588)
    else:
        return render(request, "error.html", {"error": "Method not accepted."})


@login_required
def personal_settings(request, personal):
    if request.method == "GET":
        if request.user.user_name != personal:
            return render(
                    request, "error.html",
                    {
                        "error": "Permission denied"
                    }
                )
        person = MyUser.objects.get(user_name=personal)
        form = UserChangeForm(request.POST or None, instance=person)
        return render(
                request, "common/settings.html",
                {
                    "person": person,
                    "httpsUrl": httpsUrl,
                    "imageStyle": "-avatarSetting",
                    "form": form
                }
            )
    else:
        return render(request, "404.html")


def personal_list(request, personal, status):
    if request.method == "GET":
        try:
            person = MyUser.objects.get(user_name=personal)
        except:
            return render(request, "404.html")
        else:
            return render(
                    request, "common/personal.html",
                    {
                        "person": person, "personal": personal,
                        "httpsUrl": httpsUrl, "imageStyle": "-avatarSetting",
                        "status": status
                    }
                )
    else:
        return render(request, "404.html")


@login_required
def personal_comments(request, personal):
    if request.method == "GET":
        if request.user.user_name == personal:
            return render(
                    request, "common/comments.html",
                    {
                        "httpsUrl": httpsUrl,
                        "imageStyle": "-avatarSetting"
                    }
                )
        else:
            return render(
                    request, "error.html",
                    {
                        "error": "Permission denied"
                    }
                )
    else:
        return render(request, "404.html")


def accounts(request, accounts):
    """User settings"""
    return render(request, "common/accounts.html")


def contect(request):
    """Contect Us"""
    return render(request, "common/contect.html")


@login_required
def get_notifications(request):
    if cache.get(str(request.user.id) + "_comments") == "True":
        return HttpResponse("True")
    else:
        return HttpResponse(status=204)


@login_required
def move_notifications(request):
    if cache.get(str(request.user.id) + "_comments") == "True":
        cache.set(str(request.user.id) + "_comments", "False")
    return HttpResponse(status=204)


@login_required
def get_upload_token(request):
    upload_type = request.GET.get("type")
    auth = Auth(accessKey, secretKey)
    upToken = auth.upload_token(bucket, key=None)
    sha1 = hashlib.sha1()
    serverTime = round(time.time())
    pre_key = str(request.user.id) + upload_type + secretKey[-6:]
    sha1.update(pre_key.encode("utf-8"))
    key = str(serverTime) + sha1.hexdigest()
    return JsonResponse({"token": upToken, "key": key})


@login_required
def update_posts_like(request, postId):
    error_messages = {
            1: "Sorry, you are run out of points.\
               You could get points with great posts.",
            2: "You already liked this post before.",
            3: "Something wrong with Redis server.",
            4: "Something wrong with cauculate points."
            }
    post_author_id = request.POST.get("post_author_id", "")
    post_likes_users = get_redis_connection("default")

    user_points = cache.get("user_points_" + str(request.user.id))
    # if user doesn't have enough point
    if user_points < 1:
        return HttpResponse(error_messages[1], status=500)
    # if user already like the post
    if post_likes_users.zscore(
            "post_"+str(postId),
            "user"+":"+str(request.user.id)
            ):
        return HttpResponse(error_messages[2], status=500)
    # add like to post
    try:
        post_likes_users.zadd(
                ("post_"+str(postId)),
                time.time(),
                "user"+":"+str(request.user.id)
                )
        print("post_likes")
    except:
        return HttpResponse(error_messages[3], status=500)
    else:
        try:
            cache.decr("user_points_" + str(request.user.id))
            cache.incr("user_points_" + str(post_author_id))
        except:
            return HttpResponse(error_messages[4], status=500)
    return HttpResponse(status=201)


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    email_exist = cache.get("email_" + email)
    if email_exist:
        return HttpResponse("false")
    else:
        return HttpResponse("true")


@csrf_exempt
def check_username_exist(request):
    user_name = request.POST.get("user_name")
    name_exist = cache.get("user_name_" + user_name)
    if name_exist:
        return HttpResponse("false")
    else:
        return HttpResponse("true")


@csrf_exempt
def check_act_title(request):
    act_title = request.POST.get("act_title")
    current_user = request.POST.get("current_user")
    try:
        Act.objects.get(act_title=act_title, user_id__user_name=current_user)
        return HttpResponse("false")
    except:
        return HttpResponse("true")


@csrf_exempt
def call_back(request):
    key = request.POST.get("key")
    name = request.POST.get("name")
    return JsonResponse({"key": key, "name": name})
