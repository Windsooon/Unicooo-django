from django.conf.urls import *
from activities import views

urlpatterns = [
                  url(r'^new/$', views.act_create, name='act_new'),
                  url(r'^(?P<act_list>\w+)/$', views.act_list, name="act_type"),
                  url(r'^(?P<act_author>.+)/(?P<act_title>.+)/$', views.act_details, name="act_details"),
              ]



