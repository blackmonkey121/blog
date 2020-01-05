#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from rest_framework import serializers

from .models import Post


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'category', 'desc', 'content_html', 'created_time']