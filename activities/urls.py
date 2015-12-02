#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import *
from activities import views

urlpatterns = [
                  url(r'^new/$', views.new_act),
                  url(r'^activities/$', views.ajax_act_list),
                  url(r'^(?P<act_list>\w+)/$', views.act_list, name="act_list"),
              ]


