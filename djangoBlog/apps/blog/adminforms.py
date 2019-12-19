#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django import forms

# 修改字段的展示类型
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)