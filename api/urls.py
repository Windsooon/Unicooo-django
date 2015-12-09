from django.conf.urls import *
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
                  url(r'^act/$', views.ActList.as_view()),
                  url(r'^post/$', views.PostList.as_view()),
                  url(r'^user/$', views.UserList.as_view()),
              ]

urlpatterns = format_suffix_patterns(urlpatterns)




