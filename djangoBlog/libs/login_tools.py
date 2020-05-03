#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "monkey"

from django.urls import reverse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import JsonResponse
from apps.user.models import UserInfo

from functools import wraps


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 用户名 / 手机号 / 邮箱
            user = UserInfo.objects.get(Q(username=username) | Q(phone=username) | Q(email=username))
            if user.check_password(password):
                return user

        except Exception as e:
            # TODO:日志
            return None


Au = CustomBackend()

authenticate = Au.authenticate


def required_login(func):
    @wraps(func)
    def inner(self, request, *args, **kwargs):
        """  """
        if not request.user.is_authenticated:
            self.ret['href'] = reverse('user:login')
            return JsonResponse(self.ret)
        ret = func(self, request, *args, **kwargs)
        return ret
    return inner
