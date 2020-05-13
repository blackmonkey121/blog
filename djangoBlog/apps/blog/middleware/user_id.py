#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import uuid
import re

from django.http import Http404

from apps.blog.models import Category, Tag, Post
from apps.user.models import UserInfo


USER_KEY = 'uid'    # 生成的唯一id 的 属性名
MAX_AGE = 60 * 60 * 24 * 365 * 10


class UserIDMiddleware(object):
    """
    标记用户
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):

        if request.path.startswith('/blog/post/'):
            uid = self.generate_uid(request)
            request.uid = uid
            response = self.get_response(request)
            response.set_cookie(USER_KEY, uid, max_age=MAX_AGE, httponly=True)
        else:
            response = self.get_response(request)
        return response

    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid


class GetUserMiddleware(object):
    """ 推测用户 """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):

        ret = re.match('^/blog/(?P<cls_name>\w+)/(?P<url_id>\d+)/$', request.path)   # 解析参数

        # 定义 参数 -> 类 映射字典
        cls_dict = {
            'category': Category,
            'tag': Tag,
            'post': Post,
            'home': UserInfo,
        }

        #  不满足条件的请求走正常 请求 流程
        #  1 参数格式不对
        if ret:
            ret = ret.groupdict()
            cls_name = ret.get('cls_name')
            url_id = ret.get('url_id')
        else:
            return self.get_response(request)

        # 2 参数名不匹配
        cls = cls_dict.get(cls_name, None)
        if cls is None:
            return self.get_response(request)

        # 匹配的验证是否合法，不合法抛出404 合法 绑定参数
        try:
            if issubclass(cls, UserInfo):
                user = cls.objects.filter(pk=url_id).first()
            else:
                request.cls_obj = cls.objects.filter(pk=url_id).first()
                user = cls.objects.filter(pk=url_id).first().owner

        except (AttributeError, ArithmeticError):
            # return HttpResponseNotFound()
            raise Http404

        request.visited_user = user
        request.url_id = url_id

        return self.get_response(request)

