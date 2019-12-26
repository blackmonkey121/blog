#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.conf.urls import url
from apps.user import views

urlpatterns = [
    url(r'^login', views.login,name='login'),
    url(r'^regist', views.regist,name='regist'),
    url(r'^active/(?P<token>.*)$', views.active, name='active'),
    url(r'^resetpwd', views.resetpwd, name='resetpwd')
]