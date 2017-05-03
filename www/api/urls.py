# from django.conf.urls import *
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
                  url(r"^acts/$", views.ActList.as_view()),
                  url(r"^acts/(?P<pk>[0-9]+)/$", views.ActDetail.as_view()),
                  url(r"^posts/$", views.PostList.as_view()),
                  url(r"^posts/(?P<pk>[0-9]+)/$", views.PostDetail.as_view()),
                  url(r"^users/$", views.UserList.as_view()),
                  url(r"^users/(?P<pk>[0-9]+)/$", views.UserDetail.as_view()),
                  url(r"^comments/$", views.CommentList.as_view()),
                  url(r"^comments/(?P<pk>[0-9]+)/$",
                      views.CommentDetail.as_view()),
                  url(r'^api-token-auth/', obtain_jwt_token),
              ]

urlpatterns = format_suffix_patterns(urlpatterns)
