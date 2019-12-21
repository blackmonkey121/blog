#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^category/(?P<category_id>\d+)/$', post_list, name='category_list'),
    url('^tag/(?P<tag_id>\d+)/$',post_list, name='tag_list'),
    url('^post/(?P<post_id>\d+).html$', post_detail, name='article_detail'),
]
