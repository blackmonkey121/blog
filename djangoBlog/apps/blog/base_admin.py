#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.contrib import admin


class BaseAdmin(object):
    """
    抽取Admin基类
    自动的补充owner字段
    过滤Queryset数据
    """

    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        """
        指定作者只能是当前登陆用户而不能是其他人
        :param request: 当前的请求对象
        :param obj: 当前要保存的对象
        :param form: 页面提交过来的表单对象
        :param change: 保存本次的数据是新增的还是更新的
        """
        obj.owner = request.user
        return super(BaseAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(BaseAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)