#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

import uuid


USER_KEY = 'uid'    # 生成的唯一id 的 属性名
MAX_AGE = 60 * 60 * 24 * 365 * 10


class UserIDMiddleware(object):
    """

    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY, uid, max_age=MAX_AGE, httponly=True)
        return response

    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid
