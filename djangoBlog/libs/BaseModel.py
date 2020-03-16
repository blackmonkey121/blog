#!/usr/bin/env python3
#_*_ coding: utf-8 _*_
__author__ = "monkey"

from django.db import models
from django.db.models import F
from .warps import cache_point


class BasePoint(models.Model):
    """ 点赞基类 """

    up = models.IntegerField(default=0, verbose_name='赞')
    down = models.IntegerField(default=0, verbose_name='踩')

    @classmethod
    def point_up(cls, pk: int):
        """ 赞 安全的原子操作 """
        cls.objects.filter(pk=pk).update(up=F('up') + 1)

    @classmethod
    def point_down(cls, pk: int):
        """ 踩 """
        cls.objects.filter(pk=pk).update(down=F('down') + 1)

    @classmethod
    @cache_point()
    def handle_point(cls, user=None, operate: str = None, model=None, obj: int=None):
        """ 反射拿到具体的 point 方法(up/down) """
        foo = getattr(model, 'point_{}'.format(operate))

        try:
            foo(pk=obj)
            return True, True
        except Exception as e:
            # TODO: 写入日志
            return False, '服务端错误 code:0x00'

    class Meta:
        abstract = True
