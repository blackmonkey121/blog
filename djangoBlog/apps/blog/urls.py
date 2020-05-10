#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.urls import path
from .views import *

# GetUserMiddleware 依赖 URL:post、home、tag、category 修改注意要修改URL 对应的正则表达式
# TODO：解耦 中间件对URL的依赖 <翻看源码使用 django 自己的参数解析函数>

urlpatterns = [

    path('category/<int:category_id>/', CategoryView.as_view(), name='category_list'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag_list'),
    path('post/<int:post_id>/', ArticleDetailView.as_view(), name='article_detail'),
    path('home/<int:user_id>/', HomeView.as_view(), name='home'),

    path('search/', SearchView.as_view(), name='search'),
    path('post_point/', UpArticleView.as_view(), name='article_point'),

]