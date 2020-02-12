#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, PasswordInput, CharField, EmailInput, EmailField, FileInput, Form
from .models import UserInfo
from django.utils.translation import gettext_lazy as _


class RegistForm(ModelForm):
    repassword = CharField(max_length=16,
                           min_length=2,
                           label='重复密码',
                           error_messages={
                               'min_length': _("密码最小不能少于6位"),
                               'max_length': _("密码最长不能超过16位"),
                               'required': _("重复密码不能为空")
                           },
                           widget=PasswordInput(attrs={
                               'placeholder': "重复密码"
                           })
                           )

    def clean_repassword(self):
        repassword = self.cleaned_data.get("repassword")
        password = self.cleaned_data.get("password")
        if repassword != password:
            self.add_error("repassword", ValidationError("两次密码不一致！"))
        else:
            return repassword

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not 1 < len(username) < 15:
            self.add_error('username', ValidationError("用户名应该在2～16个字符"))
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not 5 < len(password) < 15:
            self.add_error('password', ValidationError("密码应该在6～16个字符"))
        return password

    class Meta:
        model = UserInfo

        fields = [
            'username', 'password', 'email', 'phone',  # 必填
            'nickname', 'avatar'  # 选填
        ]

        widgets = {

            'username': TextInput(attrs={
                'placeholder': _('用户名/手机号/邮箱'),
            }),

            'password': PasswordInput(attrs={
                'placeholder': _('密码应该在2～16个字符'),
            }),

            'email': EmailInput(attrs={
                'placeholder': '邮箱'
            }),

            'phone': TextInput(attrs={
                'placeholder': '手机号'
            }),

            'nickname': TextInput(attrs={
                'placeholder': '昵称'
            }),

            'avatar': FileInput(attrs={

            })
        }

        error_messages = {
            'username': {
                'required': _("用户名不能为空"),
                'unique': _("用户名已被注册"),
                'invalid': _("用户名不应该包含特殊字符")
            },

            'password': {
                'required': _("密码不能为空"),
                'invalid': _("密码不应该包含特殊字符"),

            },

            'email': {
                'required': _("邮箱不能为空"),
                'invalid': _("邮箱格式不正确"),
                "unique": _("邮箱已被注册"),
            },

            'phone': {
                'required': _("手机号不能为空"),
                'invalid': _("手机号码格式不正确"),
                "unique": _("手机号已被注册"),
            },

        }


class LoginForm(Form):
    username = CharField(max_length=16,
                         min_length=2,
                         label="用户名",
                         error_messages={
                             "max_length": "用户名最长不能超过16",
                             "required": "用户名不能为空",
                             "min_length": "用户名最小不能少于2位",
                             "invalid": "不合法的用户名，不应该包含特殊字符"
                         },
                         widget=TextInput(
                             attrs={"class": "form-control",
                                    "placeholder": "账号"},
                         )

                         )
    password = CharField(max_length=16,
                         min_length=6,
                         label="密码",
                         widget=PasswordInput(
                             attrs={
                                 "placeholder": "密码"}
                         ),
                         error_messages={
                             "required": "密码不能为空",
                             "max_length": "密码最长不能超过16",
                             "min_length": "密码最短不能小于6位",
                         })


class UpdateForm(Form):
    email = EmailField(label="邮箱",
                       widget=EmailInput(
                           attrs={'placeholder': '邮箱'}
                       ),
                       error_messages={
                           'required': "邮箱不能为空",
                           "invalid": "邮箱格式不正确"
                       })


class ResetForm(ModelForm):
    new_password = CharField(max_length=16,
                             min_length=6,
                             label='新密码',
                             error_messages={
                                 'min_length': _("新密码最小不能少于6位"),
                                 'max_length': _("密码最长不能超过16位"),
                                 'required': _("新密码为必填项")
                             },
                             widget=PasswordInput(attrs={
                                 'placeholder': "新密码"
                             }))

    new_re_password = CharField(max_length=16,
                                min_length=6,
                                label='重复密码',
                                error_messages={
                                    'min_length': _("密码最小不能少于6位"),
                                    'max_length': _("密码最长不能超过16位"),
                                    'required': _("重复密码为必填项")
                                },
                                widget=PasswordInput(attrs={
                                    'placeholder': "重复密码"
                                })
                                )

    class Meta:
        model = UserInfo

        fields = ['email']

        widgets = {
            'email': EmailInput(attrs={
                'readonly': 'readonly'
            })
        }

    def clean(self):
        password = self.cleaned_data.get('new_password')
        repassword = self.cleaned_data.get('new_re_password')

        if password != repassword:
            self.add_error('new_re_password', ValidationError("两次密码不一致"))
        return self.cleaned_data
