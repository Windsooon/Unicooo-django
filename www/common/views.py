# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import connection
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from .form import UserCreateForm, UserLoginForm, UserChangeForm
from .models import CustomAuth
from activities.models import Act
from comment.models import Comment
from common.models import MyUser
from common.qiniuSettings import httpsUrl, imageStyle
from qiniu import Auth
from .qiniuSettings import *
import time
import hashlib


def dictfetchall(cursor):
    """trans tuple to dict"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def anonymous_required(view_function, redirect_to = None):
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
    act_list = Act.objects.filter(act_type=0).order_by("-act_create_time")[:9]
    imageStyle = "-actCoverSmall"
    return render(request, "common/frontpage.html", {"act_list": act_list, "httpsUrl": httpsUrl, "imageStyle": imageStyle})

@anonymous_required
def sign_up(request):
    if request.method == "GET":
        form = UserCreateForm()
        return render(request, "common/signup.html",{"form": form})
    elif request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["user_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = get_user_model().objects.create_user(username=username, email=email, password=password)
            user.save()
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
            return redirect("/")
        else:
            return render(request, "error.html", {"error": "Form is not valid."})
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
                return render(request, "error.html", {"error": "Method not accepted."})
        else:
            pass
    else:
        return render(request, "error.html", {"error": "Method not accepted."})

@login_required 
def personal_settings(request, personal):
    if request.method == "GET":
        person = MyUser.objects.get(user_name=personal)
        form = UserChangeForm(request.POST or None, instance=person)
        return render(request, "common/settings.html", {"person": person, "form": form})
    else:
        return render(request, "404.html")

def personal_list(request, personal, status):
    if request.method == "GET":
        try:
            person = MyUser.objects.get(user_name=personal)
        except: 
            return render(request, "404.html")
        else:
            return render(request, "common/personal.html", {"person": person, "personal": personal, "status": status})
    else:
        return render(request, "404.html")

def personal_comments(request, personal):
    if request.method == "GET":
        if request.user.user_name == personal:
            return render(request, "common/comments.html")
        else: 
            return render(request, "error.html", {"error": "Not allow"})
    else:
        return render(request, "404.html")

def accounts(request, accounts):
    """User settings"""
    return render(request, "common/accounts.html")

def contect(request):
    """Contect Us"""
    return render(request, "common/contect.html")

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

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email");
    try:
        MyUser.objects.get(email=email)
        return HttpResponse("false")
    except:
        return HttpResponse("true")

@csrf_exempt
def check_username_exist(request):
    user_name = request.POST.get("user_name");
    try:
        MyUser.objects.get(user_name=user_name)
        return HttpResponse("false")
    except:
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


