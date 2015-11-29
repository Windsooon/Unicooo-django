#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import *
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('common.urls')),
    url(r'^act/', include('activities.urls')),

]
