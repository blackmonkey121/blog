#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.conf.urls import url
from ..config.views import FavoriteView

urlpatterns = [
    url('^favorite/$', FavoriteView.as_view(), name='favorite'),
]