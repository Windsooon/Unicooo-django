import json
from django.shortcuts import render, redirect
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ActForm
from .models import Act
from post.models import Post
from common.models import MyUser

#--------------#
#carate new activity
#--------------#
def new_act(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            form = ActForm()
            return render(request, "act/new.html", {"form": form})
        else:
            redirect('/login/') 
    elif request.method == "POST":
        if request.user.is_authenticated():
            form = ActForm(request.POST)
            if form.is_valid():
                act_ident = Act.objects.all().aggregate(Max('act_ident'))["act_ident__max"] + 1
                act = form.save(commit=False)
                act.act_ident = act_ident
                act_type = form.cleaned_data["act_type"]
                act_licence = form.cleaned_data["act_licence"]
                act_title = form.cleaned_data["act_title"]
                act_username = request.user.user_name
                act.act_type = act_type
                act.act_licence = act_licence
                act.user_id = request.user.id
                act.act_url = "/act/" + act_username + "/" + act_title
                act.save()
                error = 'hey'
                return render(request, "error.html", {"error": error})
    else:
        error = "不允许使用此方法。"
        return render(request, "error.html", {"error": error})

def act_list(request, act_list):
    if request.method == "GET":
        if act_list in ("public", "group", "personal"):
            dict_act = {"public": 0, "group": 1, "personal": 2}
            act_details = Act.objects.filter(act_type=dict_act[act_list])[:9]
            return render(request, "act/activities_list.html", {"act_list": act_details})
        else:
            error = "不存在此分类。"
            return render(request, "error.html", {"error": error})
    else:
        error = "不允许使用此方法。"
        return render(request, "error.html", {"error": error})


#--------------#
#show activities details
#--------------#
def act_details(request, act_author, act_title):
    if request.method == "GET":
        try:
            act_author_id = MyUser.objects.get(user_name=act_author).id
            act_details = Act.objects.get(act_title=act_title, user_id=act_author_id)
        except:
            error = "不存在此活动。"
            return render(request, "error.html", {"error": error})
        else:
            act_posts = Post.objects.filter(act_id=act_details.id)
            return render(request, "act/activities_details.html", {"act_details": act_details, "act_posts": act_posts})
    else:
        error = "不允许使用此方法。"
        return render(request, "error.html", {"error": error})


#--------------#
#show activities list
#--------------#
def ajax_act_list(request):
    act_type = request.GET.get("act_type", None)
    page = request.GET.get("page", None)
    number = request.GET.get("number", None)
    ajax_act_list = Act.objects.filter(act_type=act_type)
    paginator = Paginator(ajax_act_list, number)
    try:
        act_list = paginator.page(page)
    except PageNotAnInteger:
        act_list = paginator.page(1)
    except EmptyPage:
        act_list = paginator.page(paginator.num_pages)
    act_list = json.dumps(act_list)
    return render(request, "act/activities_list.html", {"act_list": act_list})

    
