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
                  url(r'^signup/$',views.sign_up),
                  url(r'^login/$',views.login_in),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

