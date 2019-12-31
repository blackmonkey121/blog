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
from django.views.static import serve
from apps.blog.views import IndexView
from apps.blog.branch_site import branch_site
from apps.user.views import login

urlpatterns = [
    url(r'^media/(?P<path>.*)', serve, {"document_root": develop.MEDIA_ROOT}),
    url(r'^user/', include('apps.user.urls', namespace='user')),
    url(r'^blog/', include('apps.blog.urls', namespace='blog')),
    url(r'^super_admin/', admin.site.urls, name='super_admin'),
    url(r'^user_admin/', branch_site.urls, name='user_admin'),
    url(r'^config/', include('apps.config.urls', namespace='config')),
    url(r'^', IndexView.as_view(), name="index"),
]
