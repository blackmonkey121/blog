#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.conf.urls import url
from .views import CommentView, UpCommentView

urlpatterns = [
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^comment_point/$', UpCommentView.as_view(), name='comment_point'),
]