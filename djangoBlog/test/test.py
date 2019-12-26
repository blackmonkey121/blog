#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

#
# import os
#
# from django.core.urlresolvers import reverse
# import django
#
# if __name__ == "__main__":
#
#     PROFILE_LIST = {1: 'develop',
#                     2: 'product'}
#
#     profile = os.environ.get('PROJECT_PROFILE', PROFILE_LIST.get(1,2))
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE','djangoBlog.settings.{}'.format(profile))
#
#     django.setup()

my_dict = {'csrfmiddlewaretoken': ['fKFkQSueK1aeQTAuAq0ul9coIOBryejXVVrL1cZMpgLysbnn3ft72mLLnoljfcfI'], 'username': ['赵宇'], 'password': [['monkey123'], ['monkey123']], 'email': ['931976722@qq.com'], 'phone': ['15526327936'], 'nickname': ['小师弟'], 'avatar': ['']}


def func(*args):
    print(args)

x = ['monkey','hook']
func(*x)
