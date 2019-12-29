#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category_list'),
    url(r'^tag/(?P<tag_id>\d+)/$',TagView.as_view(), name='tag_list'),
    url(r'^post/(?P<post_id>\d+).html$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^test$',test)

]
