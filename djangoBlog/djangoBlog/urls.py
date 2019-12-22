"""djangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from djangoBlog.settings import develop
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.staticfiles.views import serve

from apps.blog.branch_site import branch_site


urlpatterns = [
    url(r'^super_admin/', admin.site.urls, name='super_admin'),
    url(r'^user_admin/', branch_site.urls, name='user_admin'),
    url(r'^user/', include('apps.user.urls', namespace='user')),
    url(r'^blog/', include('apps.blog.urls', namespace='blog')),
    url(r'^config/', include('apps.config.urls', namespace='config')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": develop.MEDIA_ROOT}),
]
