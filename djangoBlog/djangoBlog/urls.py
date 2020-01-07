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
from django.views.static import serve
from django.contrib.sitemaps import views as sitemap_views
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from .RSS import LastesPostFeed
from .sitemap import PostSitemap
from apps.blog.views import IndexView
from apps.blog.apis import ArticleViewSet, CategoryViewSet
import xadmin

router = DefaultRouter()
router.register(r'post',ArticleViewSet, basename='api_article')
router.register(r'category', CategoryViewSet, basename='api_category')


urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/docs/', include_docs_urls(title='Monkey Blog apis')),

    url(r'^user/', include('apps.user.urls', namespace='user')),
    url(r'^blog/', include('apps.blog.urls', namespace='blog')),
    url(r'^config/', include('apps.config.urls', namespace='config')),
    url(r'^comment/', include('apps.comment.urls', namespace='comment')),

    url(r'^ckeditor/', include('ckeditor_uploader.urls'),),
    url(r'^media/(?P<path>.*)', serve, {"document_root": develop.MEDIA_ROOT}),

    url(r'^admin/', xadmin.site.urls, name='xadmin'),

    url(r'^RSS|feed/', LastesPostFeed(), name='RSS'),
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts':PostSitemap}}),

    url(r'^', IndexView.as_view(), name="index"),
]
