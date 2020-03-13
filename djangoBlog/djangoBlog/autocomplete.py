#!/usr/bin/env python3
#_*_ coding: utf-8 _*_
__author__ = "monkey"

from dal import autocomplete

from apps.blog.models import Category, Tag

class CategoryAutoComplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Category.objects.none()

        qs = Category.objects.filter(owner=self.request.user)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TagAutoComplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tag.objects.none()

        qs = Tag.objects.filter(owner=self.request.user)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
