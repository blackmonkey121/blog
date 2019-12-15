#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.conf.urls import url
from apps.user import views

urlpatterns = [
    url(r'^login', views.login)
]