
from djangoBlog.settings import setting
from django.urls import path, include, re_path
from django.views.static import serve
from django.contrib.sitemaps import views as sitemap_views
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from .RSS import LastesPostFeed
from .sitemap import PostSitemap
from apps.blog.views import IndexView
from apps.blog.apis import ArticleViewSet, CategoryViewSet
import xadmin
from .autocomplete import CategoryAutoComplete, TagAutoComplete

router = DefaultRouter()
router.register(r'post',ArticleViewSet, basename='api_article')
router.register(r'category', CategoryViewSet, basename='api_category')


urlpatterns = [
    path('api/', include((router.urls, 'rest_framework'), namespace='api')),
    path('api/docs/', include_docs_urls(title='Monkey Blog apis')),

    path('user/', include(('apps.user.urls', 'user'), namespace='user')),
    path('blog/', include(('apps.blog.urls', 'blog'), namespace='blog')),
    path('config/', include(('apps.config.urls', 'config'), namespace='config')),
    path('comment/', include(('apps.comment.urls', 'comment'), namespace='comment')),

    path('ckeditor/', include(('ckeditor_uploader.urls'))),
    path('category-autocomplete/', CategoryAutoComplete.as_view(), name='category-autocomplete'),
    path('tag-autocomplete/', TagAutoComplete.as_view(), name='tag-autocomplete'),

    # path('media/<str:path>', serve, {"document_root": develop.MEDIA_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': setting.MEDIA_ROOT}),

    path('admin/', xadmin.site.urls, name='xadmin'),

    path('RSS', LastesPostFeed(), name='rss'),
    path('sitemap\.xml', sitemap_views.sitemap, {'sitemaps': {'posts':PostSitemap}}),

    path('', IndexView.as_view(), name="index"),
]

from libs import exception_func

handler400 = exception_func.bad_request
handler403 = exception_func.permission_denied
handler404 = exception_func.page_not_found
handler500 = exception_func.server_error


if setting.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__', include(debug_toolbar.urls)),
    ] + urlpatterns