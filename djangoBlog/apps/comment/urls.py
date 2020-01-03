#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.conf.urls import url
from .views import CommentView

urlpatterns = [
    url(r'^comment/$', CommentView.as_view(), name='comment'),
]