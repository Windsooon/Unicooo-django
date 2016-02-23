import json
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ActCreateForm
from .models import Act
from post.models import Post
from common.models import MyUser

#--------------#
#create new activity
#--------------#
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to create activity
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(data)
        else:
            return response

def act_create(request):
    if request.method == "GET":
        form = ActCreateForm
        return render(request, "act/new.html", {"form": form})
#class ActCreate(LoginRequiredMixin, CreateView):
#    login_url = '/login/'
#    redirect_field_name = 'redirect_to'
#    model = Act
#    template_name = "act/new.html"
#    form_class = ActCreateForm
    
def act_list(request, act_list):
    if request.method == "GET":
        url = "https://o2ocy30id.qnssl.com/"
        style_name = "-actCoverInterS"
        if act_list in ("public", "group", "personal"):
            dict_act = {"public": 0, "group": 1, "personal": 2}
            act_details = Act.objects.filter(act_type=dict_act[act_list])[:12]
            return render(request, "act/activities_list.html", {"act_list": act_details, "url": url, "style_name": style_name})
        else:
            error = "不存在此分类。"
            return render(request, "error.html", {"error": error})
    else:
        error = "不允许使用此方法。"
        return render(request, "error.html", {"error": error})


#----------------------#
#show activities details
#----------------------#
def act_details(request, act_author, act_title):
    if request.method == "GET":
        try:
            act_author_id = MyUser.objects.get(user_name=act_author).id
            act_details = Act.objects.get(act_title=act_title, user_id=act_author_id)
        except:
            error = "不存在此活动。"
            return render(request, "error.html", {"error": error})
        else:
            act_posts = Post.objects.filter(act_id=act_details.id)[:12]
            return render(request, "post/posts_list.html", {"act_details": act_details})
    else:
        error = "不允许使用此方法。"
        return render(request, "error.html", {"error": error})


