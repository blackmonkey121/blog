#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


class BaseAdmin(object):
    """
    抽取Admin基类
    自动的补充owner字段
    过滤Queryset数据
    """

    exclude = ('owner',)

    def save_models(self):
        """
        指定作者只能是当前登陆用户而不能是其他人
        """
        self.new_obj.owner = self.request.user
        return super().save_models()

    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)