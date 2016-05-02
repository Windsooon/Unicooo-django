#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from common import views

urlpatterns = [
                  url(r'^$',views.front_page),
                  url(r'^public-activities/$',views.public_activities),
                  url(r'^sub/$',views.get_notifications),
                  url(r'^sub_no/$',views.move_notifications),
                  url(r'^token/$',views.get_upload_token),
                  url(r'^likes/(?P<postId>\d+)/$',views.update_posts_like),
                  url(r'^email/$',views.check_email_exist),
                  url(r'^checkuser/$',views.check_username_exist),
                  url(r'^act_title/$',views.check_act_title),
                  url(r'^callback/$',views.call_back),
                  url(r'^signup/$', views.sign_up, name="sign_up"),
                  url(r'^login/$', views.login_in, name="login"),
                  url(r'^contect/$', views.contect, name="contect"),
                  url(r'^(?P<personal>.[^/]+)/comments/$', views.personal_comments, name="comments"),
                  url(r'^(?P<personal>.[^/]+)/(?P<status>\w+)/$', views.personal_list, name="status"),
                  url(r'^(?P<personal>.[^/]+)/$', views.personal_settings, name="personal"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

