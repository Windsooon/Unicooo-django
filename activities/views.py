import json
from django.shortcuts import render, redirect
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ActForm
from .models import Act

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
            error = "不存在。"
            return render(request, "error.html", {"error": error})
    else:
        error = "不允许使用此方法。"
        return render(request, "error.html", {"error": error})

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
    print (act_list)
    return render(request, "act/activities_list.html", {"act_list": act_list})

    
