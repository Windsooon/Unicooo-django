#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import *
from django.contrib import admin

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^api/", include("api.urls")),
    url(r"^act/", include("activities.urls")),
    url(r"^post/", include("post.urls")),
    url(r"^", include("common.urls")),

]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
