#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Post


class PostSitemap(Sitemap):
    changefreq = "always"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return reverse('blog:article_detail', args=[obj.pk])


