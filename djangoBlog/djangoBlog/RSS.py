#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from apps.blog.models import Post


class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.addQuickElement('content:html',item['content_html'])


class LastesPostFeed(Feed):
    feed_type = ExtendedRSSFeed
    title = 'Monkey Blog System'
    link = '/rss/'
    description = "Monkey is a blog system power by django"

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('blog:article_detail', args=[item.pk])

    def item_extra_kwargs(self, item):
        return {'content_html':self.item_content_html(item)}

    def item_content_html(self, item):
        return item.content_html

