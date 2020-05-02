#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.urls import path
from .views import *

# app_name = 'blog'

urlpatterns = [

    path('category/<int:category_id>)/', CategoryView.as_view(), name='category_list'),
    path('tag/<int:tag_id>)/', TagView.as_view(), name='tag_list'),
    path('post/<int:post_id>).html', ArticleDetailView.as_view(), name='article_detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('post_point/', UpArticleView.as_view(), name='article_point'),
    path('<int:user_id>', IndexView.as_view(), name='home'),

]