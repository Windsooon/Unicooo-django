#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^act/", include("activities.urls")),
    url(r"^api/", include("api.urls")),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r"^", include("common.urls")),
]
