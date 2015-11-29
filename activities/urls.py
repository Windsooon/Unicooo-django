#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import *
from activities import views

urlpatterns = [
                  url(r'^new',views.new_act),
                  #url(r'^act/(?P<user>)/(?P<activity>)/$',views.front_page),
              ]


