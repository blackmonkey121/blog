#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.urls import path
from ..config.views import FavoriteView

urlpatterns = [
    path('favorite/', FavoriteView.as_view(), name='favorite'),
]