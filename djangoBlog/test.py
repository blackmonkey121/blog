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



