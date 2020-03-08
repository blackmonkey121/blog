#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.conf.urls import url
from .views import LoginView, RegistView, UpdatePassWordView,LogoutView, ActiveView, ResetView


urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^regist/', RegistView.as_view(), name='regist'),
    url(r'^logout/',LogoutView.as_view(), name='logout'),

    url(r'^update/', UpdatePassWordView.as_view(), name='update'),
    url(r'^reset/(?P<token>.*)$', ResetView.as_view(), name='reset'),
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),
]