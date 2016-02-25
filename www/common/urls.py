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
                  url(r'^token/$',views.get_upload_token),
                  url(r'^callback/$',views.call_back),
                  url(r'^signup/$', views.sign_up),
                  url(r'^login/$', views.login_in),
                  url(r'^(?P<personal>\w+)/$', views.personal, name="personal"),
                  url(r'^(?P<personal>\w+)/(?P<status>\w+)/$', views.personal_list, name="settings"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

