#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from common import views

urlpatterns = [
                  url(r'^$', views.front_page, name="front_page"),
                  url(r'^sub/$', views.get_notifications),
                  url(r'^sub_no/$', views.move_notifications),
                  url(r'^token/$', views.get_upload_token),
                  url(r'^likes/(?P<postId>\d+)/$', views.update_posts_like),
                  url(r'^checkemail/$', views.check_email_exist),
                  url(r'^checkuser/$', views.check_username_exist),
                  url(r'^act_title/$', views.check_act_title),
                  url(r'^signup/$', views.sign_up, name="sign_up"),
                  url(r'^login/$', views.login_in, name="login"),
                  url(r'^contact/$', views.contact, name="contact"),
                  url(r'^logout/$', views.logout_user, name="logout"),
                  url(r'^(?P<personal>.[^/]+)/comments/$',
                      views.personal_comments, name="comments"),
                  url(r'^(?P<personal>.[^/]+)/(?P<status>act_create|act_join|post)/$',
                      views.personal_list, name="status"),
                  url(r'^(?P<personal>.[^/]+)/settings/$',
                      views.personal_settings, name="personal_settings"),
                  url(r'^(?P<personal>.[^/]+)/$',
                      views.personal, name="personal"),
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)
