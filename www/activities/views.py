from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from common.qiniuSettings import httpsUrl, imageStyle, avatarStyle
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

@login_required 
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
        url = "https://o3e6g3hdp.qnssl.com/"
        style_name = "-actCoverInterS"
        act_details = Act.objects.filter(act_type=2)[:12]
        return render(request, "act/activities_list.html", {"act_list": act_details, "url": url, "style_name": style_name})
    else:
        error = "不允许使用此方法。"
        return render(request, "error.html", {"error": error})


#----------------------#
#show activities details
#----------------------#
def act_details(request, act_author, act_title):
    if request.method == "GET":
        try:
            act_author = MyUser.objects.get(user_name=act_author)
            act_details = Act.objects.get(act_title=act_title, user_id=act_author.id)
        except:
            error = "不存在此活动。"
            return render(request, "error.html", {"error": error})
        else:
            act_thumb =  httpsUrl + act_details.act_thumb_url + imageStyle
            return render(request, "post/posts_list.html", {"act_details": act_details, "act_author": act_author, "act_thumb": act_thumb, "httpsUrl": httpsUrl, "imageStyle": imageStyle, "avatarStyle": avatarStyle})
    else:
        error = "不允许使用此方法。"
        return render(request, "error.html", {"error": error})


