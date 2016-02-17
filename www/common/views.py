# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import connection
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from .form import UserCreateForm, UserLoginForm
from .models import CustomAuth
from qiniu import Auth
import time


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
    cursor = connection.cursor()
    cursor.execute("SELECT act_title, act_content, act_thumb_url, act_type, CASE WHEN act_type=0 THEN 'public' WHEN act_type=1 THEN 'group' ELSE 'personal' END AS act_type_str, a.user_name FROM ( SELECT ROW_NUMBER() OVER " +
                   "(PARTITION BY act_type ORDER BY act_create_time ) AS r, t.* FROM activities_act t) x , common_user a WHERE x.r <= 3 and user_id = a.id;")
    act_list = dictfetchall(cursor)
    return render(request, "common/frontpage.html", {"act_list": act_list})

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
        else:
            pass
    else:
        return render(request, "error.html", {"error": "Method not accepted."})

def personal(request, personal):
    if request.method == "GET":
        return render(request, "common/personal.html", {"personal": personal})
    else:
        return render(request, "404.html")

def accounts(request, accounts):
    """User settings"""
    return render(request, "common/accounts.html")

accessKey = "jBYdJ5zP1rWc2KfUWlsXAe8FD0sFyALSzyaPI8Ys" 
secretKey = "XvIPtijF_b7LMrsB7c2FNpqMiqRxG7tyyH217lej"
bucket = "uni-image-test"

@login_required 
def get_upload_token(request):
    auth = Auth(accessKey, secretKey)
    upToken = auth.upload_token(bucket, key=None)
    serverTime = time.time()
    return JsonResponse({"token": upToken, "key": serverTime})

