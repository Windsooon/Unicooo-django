#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
import debug_toolbar

urlpatterns = [
    url(r'^silk/', include('silk.urls', namespace='silk')),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^act/", include("activities.urls")),
    url(r"^api/", include("api.urls")),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r"^", include("common.urls")),

]

urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
