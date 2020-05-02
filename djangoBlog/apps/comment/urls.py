#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.urls import path
from .views import CommentView, UpCommentView

urlpatterns = [
    path(r'comment/', CommentView.as_view(), name='comment'),
    path(r'comment_point/', UpCommentView.as_view(), name='comment_point'),
]