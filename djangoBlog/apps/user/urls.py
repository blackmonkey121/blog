#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.urls import path
from .views import LoginView, RegistView, UpdatePassWordView,LogoutView, ActiveView, ResetView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('regist/', RegistView.as_view(), name='regist'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('update/', UpdatePassWordView.as_view(), name='update'),
    path('reset/<str:token>/', ResetView.as_view(), name='reset'),
    path('active/<str:token>/', ActiveView.as_view(), name='active'),
]