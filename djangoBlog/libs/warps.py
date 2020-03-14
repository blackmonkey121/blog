#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "monkey"
from django.core.cache import cache
from functools import wraps


def cache_warp(instance=cache):
    """
    函数级 缓存装饰器
    """
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