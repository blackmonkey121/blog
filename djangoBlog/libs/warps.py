#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
__author__ = "monkey"

from django.core.cache import cache
from functools import wraps


def cache_wrap(instance=cache, timeout=60):
    """
    函数级 缓存装饰器
    params instance: 缓存实例， 需要提供get set 方法，默认为 django.core.cache.cache
    params timeout: 缓存过期时间
    """
    def middle(func):
        @wraps(func)
        def inner(*args, **kwargs):
            """
            使用函数id 和 其所有的参数生成 key return 为 值 存入缓存，
            命中则直接返回结果 没有命中 执行函数 并将结果存入缓存
            """
            elem = lambda x, y: str(x) + str(y)
            key_func = hash(id(func))
            key_args = hash(args)
            key_kwargs = hash(''.join([elem(i,j) for i,j in kwargs.items()]))
            unique_key = str(hash(key_args+key_kwargs+key_func))   # 生成唯一的键

            obj = instance.get(unique_key)  # 获取值

            if obj is None:  # 未命中 则计算
                obj = func(*args, **kwargs)
                instance.set(unique_key, obj, timeout=timeout)  # 写入缓存
            return obj

        return inner
    return middle


def cache_point(instance=cache, timeout=24 * 60 * 60):
    """
    点赞装饰器
    params instance: 缓存对象， 对象应该提供get 和 set API
    params timeout: 缓存过期时间 默认为 1 天
    """
    def middle(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = kwargs.get('user')  # 点赞人id
            operate = kwargs.get('operate')   # 赞 / 踩 up/ down
            obj = kwargs.get('obj')   # 点赞的对象
            model = kwargs.get('model')   # 点赞的表

            if all((user, operate, obj, model)):  # 信息是否完整
                unique_key = str(hash(str(user)+model.__name__+str(obj)))  # 生成唯一的 key
            else:
                raise KeyError('该装饰器装饰的函数必须使用关键字传参，且user, operate, obj_id, model 是必须的。')

            obj = instance.get(unique_key)
            if obj is None:
                obj = func(*args, **kwargs)
                instance.set(unique_key, '', timeout=timeout)
            else:
                obj = False, '点一下就得了！！！'
            return obj
        return inner
    return middle