#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

# 定制Site
from django.contrib.admin import AdminSite


class BranchSite(AdminSite):
    site_header = 'djangoBlog'
    site_title = 'djangoBlog 后台管理页面'
    index_title = '首页'


branch_site = BranchSite(name='branch_admin')