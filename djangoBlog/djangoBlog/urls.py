
from djangoBlog.settings import develop
from django.urls import path, include
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

    path('ckeditor/', include(('ckeditor_uploader.urls', 'ckeditor')),),

    path('category-autocomplete/', CategoryAutoComplete.as_view(), name='category-autocomplete'),
    path('tag-autocomplete/', TagAutoComplete.as_view(), name='tag-autocomplete'),

    path('media/<str:path>', serve, {"document_root": develop.MEDIA_ROOT}),

    path('admin/', xadmin.site.urls, name='xadmin'),

    path('RSS', LastesPostFeed(), name='rss'),
    path('sitemap\.xml', sitemap_views.sitemap, {'sitemaps': {'posts':PostSitemap}}),

    path('', IndexView.as_view(), name="index"),
]

from djangoBlog.settings import develop

if develop.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__', include(debug_toolbar.urls)),
    ] + urlpatterns