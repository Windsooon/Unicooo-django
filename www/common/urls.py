#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.views.decorators.cache import cache_page
from common import views

urlpatterns = [
    url(r'^$', cache_page(60 * 1)(views.front_page),
        name="front_page"),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^check_old_password/$',
        views.check_old_password, name='check_old_password'),
    url(r'^sub/$', views.get_notifications),
    url(r'^sub_no/$', views.move_notifications),
    url(r'^token/$', views.get_upload_token),
    url(r'^how-to/$', views.how_to),
    url(r'^likes/(?P<post_id>\d+)/$', views.update_posts_like),
    url(r'^checkemail/$', views.check_email_exist),
    url(r'^privacy/$',
        cache_page(60 * 15)(views.privacy), name="privacy"),
    url(r'^question/$',
        cache_page(60 * 15)(views.question), name="question"),
    url(r'^checkuser/$', views.check_username_exist),
    url(r'^thanks/$',
        cache_page(60 * 15)(views.thanks), name="thanks"),
    url(r'^act_title/$', views.check_act_title),
    url(r'^signup/$',
        views.sign_up, name="sign_up"),
    url(r'^login/$',
        views.login_in, name="login"),
    url(r'^contact/$',
        cache_page(60 * 15)(views.contact), name="contact"),
    url(r'^logout/$', views.logout_user, name="logout"),
    url(r'^(?P<personal>.[^/]+)/comments/$',
        views.personal_comments, name="comments"),
    url(r'^(?P<personal>.[^/]+)/feed/$',
        views.personal_feed, name="feed"),
    url(r'^(?P<personal>.[^/]+)/(?P<status>' +
        r'act_create|act_join|post)/$',
        views.personal_list, name="status"),
    url(r'^(?P<personal>.[^/]+)/settings/$',
        views.personal_settings, name="personal_settings"),
    url(r'^(?P<personal>.[^/]+)/$',
        views.personal, name="personal"),
]
