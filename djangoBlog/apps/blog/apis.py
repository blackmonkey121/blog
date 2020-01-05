#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post
from .Serializers import PostSerializers


class ArticleList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializers