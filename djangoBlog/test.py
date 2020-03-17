#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


import os

from django.core.urlresolvers import reverse
import django

if __name__ == "__main__":

    PROFILE_LIST = {1: 'develop',
                    2: 'product'}

    profile = os.environ.get('PROJECT_PROFILE', PROFILE_LIST.get(1,2))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','djangoBlog.settings.{}'.format(profile))

    django.setup()

from functools import wraps


class Cache():
    """ 模拟缓存API """
    def __init__(self):
        self.con = {}

    def get(self, k):
        """"""
        return self.con.get(k, None)

    def set(self, k, v):
        """"""
        self.con[k] = v


cache = Cache()  # 缓存实例


def cache_warp(instance=cache):
    def middle(func):
        @wraps(func)
        def inner(*args, **kwargs):
            elem = lambda x, y: str(x) + str(y)
            key_func = hash(id(func))
            key_args = hash(args)
            key_kwargs = hash(''.join([elem(i,j) for i,j in kwargs.items()]))
            unique_key = str(hash(key_args+key_kwargs+key_func))

            obj = instance.get(unique_key)
            if obj is None:
                obj = func(*args, **kwargs)
                instance.set(unique_key, obj)
            return obj
        return inner
    return middle

@cache_warp(instance=cache)
def test(*args, **kwargs):
    return args, kwargs


for i in range(10):
    test(i,i)

print(cache.con)
