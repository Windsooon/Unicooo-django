from django.shortcuts import render, redirect
from .form import UserCreateForm, UserLoginForm
from django.contrib.auth import get_user_model
from django.db import connection
from .models import CustomAuth
from django.contrib.auth import authenticate, login as django_login


def dictfetchall(cursor):
    """把tuple类型转换成字典类型"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def public_activities(request):
    render(request, "public_activities.html")

def front_page(request):
    cursor = connection.cursor()
    cursor.execute("SELECT act_title, act_content, act_thumb_url,  a.user_name FROM ( SELECT ROW_NUMBER() OVER " +
                   "(PARTITION BY act_type ORDER BY act_create_time ) AS r, t.* FROM activities_act t) x , common_user a WHERE x.r <= 3 and user_id = a.id;")
    act_list = dictfetchall(cursor)
    return render(request, "common/frontpage.html", {"act_list": act_list})

def sign_up(request):
    if request.method == "GET":
        form = UserCreateForm()
        return render(request, "signup.html",{"form": form})
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
            return render(request, "404.html")
    else:
        return render(request, "404.html")

def login_in(request):
    if request.method == "GET":
        form = UserLoginForm()
        return render(request, "login.html", {"form": form})
    elif request.method == "POST":
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return redirect("/")
        else:
            pass
    else:
        return render(request, "404.html")

    
