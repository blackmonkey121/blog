#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.conf.urls import url
from ..config.views import *

urlpatterns = [
    url('^links/$', links),
]