#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from rest_framework import viewsets
from .models import Post, Category
from .Serializers import ArticleSerializer, ArticleDetailSerializer, CategorySerializer, CategoryDetailSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = ArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ArticleDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)


