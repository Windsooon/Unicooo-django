from django.conf.urls import *
from activities import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
                  url(r'^new/$', views.ActCreate.as_view(), name='act_new'),
                  url(r'^activities/$', views.ajax_act_list),
                  url(r'^(?P<act_list>\w+)/$', views.act_list, name="act_list"),
                  url(r'^(?P<act_author>\w+)/(?P<act_title>\w+)/$', views.act_details, name="act_details"),
              ]

urlpatterns = format_suffix_patterns(urlpatterns)


