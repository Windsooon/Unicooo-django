from django.conf.urls import url
from activities import views

urlpatterns = [
                  url(r'^new/$', views.act_create, name='act_new'),
                  url(r'^(?P<act_intro>.+)/' +
                      r'(details)/$',
                      views.act_intro, name='act_intro'),
                  url(r'^(?P<act_list>\w+)/$',
                      views.act_list, name='act_type'),
                  url(r'^(?P<act_url>.+)/$',
                      views.act_details, name='act_details'),
              ]
