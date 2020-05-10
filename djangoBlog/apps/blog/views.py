import logging

from django.core.cache import cache
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, View
from django.urls import reverse
from django.db.models import Q, F
from datetime import date

from .models import Post, Tag, Category
from apps.config.models import Link, Favorite
from libs.login_tools import required_login

# Create your views here.
from ..comment.models import Comment

logger = logging.getLogger(__name__)


class BaseViewMixin(object):
    """ 为Index、HomeView、TagView、CategoryView、Detail添加通用数据 """

    page_flag = None

    @staticmethod
    def get_query():
        return Post.objects.filter(status=Post.STATUS_NORMAL).select_related('category', 'owner')

    def get_queryset(self, **kwargs):
        return self.get_query()

    def update_home_context(self, context):

        category_list = Category.objects.filter(owner_id=self.request.visited_user, status=Category.STATUS_NORMAL)
        tag_list = Tag.objects.filter(owner=self.request.visited_user, status=Tag.STATUS_NORMAL)
        link_list = Link.objects.filter(owner=self.request.visited_user, status=Link.STATUS_NORMAL)
        favorite_list = Favorite.objects.filter(owner=self.request.visited_user, status=Favorite.STATUS_NORMAL)

        context.update({
            'category_list': category_list,
            'tag_list': tag_list,
            'link_list': link_list,
            'favorite_list': favorite_list,
            'visited_user': self.request.visited_user,
        })

        return context

    def update_Index_content(self, context):
        hot_article = self.get_query().order_by('-pv')[:10]
        latest_article = self.get_query()[:10]  # 默认的order_by ['-id']
        context.update({
            'hot_article': hot_article,
            'latest_article': latest_article
        })
        return context


class IndexView(BaseViewMixin, ListView):
    """ 主页 最新的文章、最热的文章、推荐文章 """

    paginate_by = 5

    context_object_name = "article_list"

    template_name = "blog/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)

        context.update({'page_title': 'Monkey Blog 首页'})

        return self.update_Index_content(context)


class HomeView(BaseViewMixin, ListView):
    """ 个人的最新文章、最热文章、分类、标签、个人信息、 """

    paginate_by = 10

    context_object_name = "article_list"

    template_name = "blog/article_list.html"

    def get_query(self):
        qs = super().get_query()
        return qs.filter(owner=self.request.visited_user)

    def get_queryset(self, **kwargs):
        qs = super(HomeView, self).get_queryset()
        return qs.filter(owner=self.request.visited_user)

    def get_context_data(self, *, object_list=None, **kwargs):
        """ """
        context = super(HomeView, self).get_context_data(**kwargs)  # {hot_article, latest_article, article_list}

        context = self.update_Index_content(context)  # 最热 最新 文章

        context.update({'page_title': '%s的主页' % (self.request.visited_user.nickname or self.request.visited_user.username) })

        return self.update_home_context(context)  # 分类


class CategoryView(HomeView):
    """ 分类页面, 按照分类列出文章 """

    def get_query(self):

        qs = super(CategoryView, self).get_query()
        return qs.filter(category=self.request.url_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context.update({'page_title': '分类页: %s' % self.request.cls_obj.name})
        return context


class TagView(HomeView):
    """ 标签页面， 按照标签列出文章 """

    def get_query(self):
        qs = super(TagView, self).get_query()
        return qs.filter(tag=self.request.url_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        context.update({'page_title': '标签页: %s' % self.request.cls_obj.name})
        return context


class ArticleDetailView(BaseViewMixin, DetailView):
    """ 文章详情页 """

    template_name = 'blog/article_detail.html'
    context_object_name = "article"

    def get_query(self):
        """ 过滤边栏数据 """
        qs = super(ArticleDetailView, self).get_query()
        return qs.filter(owner=self.request.visited_user)

    def get_object(self, queryset=None):
        """ 优化查询 加载外键字段 """
        obj = Post.objects.filter(pk=self.request.url_id).select_related('category', 'owner').get()
        return obj

    def get(self, request, *args, **kwargs):

        response = super().get(request, *args, **kwargs)
        self.handle_visited(request)
        return response

    def handle_visited(self, request):
        """"""
        increase_pv = False
        increase_uv = False

        uid = request.uid
        pv_key = 'pv:{}:{}'.format(uid, self.request.path)
        uv_key = 'uv:{}:{}'.format(uid, str(date.today()), self.request.path)

        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)  # 60s

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(pv_key, 1, 24 * 60 * 60)  # 24H

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)  # 保证+1的原子性
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.update_Index_content(context)
        context = self.update_home_context(context)
        context.update({
            'comments': Comment.objects.filter(target=self.request.url_id).order_by('-id').select_related('owner'),
            'page_title': '%s详情页' % self.request.cls_obj.title
        })
        return context


class SearchView(IndexView):
    """ 整站搜索 """

    def get_queryset(self):
        query_set = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if keyword:
            return query_set.filter(Q(title__contains=keyword) | Q(desc__contains=keyword))
        return query_set

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return content


class UpArticleView(View):

    def __init__(self):
        self.ret = {"status": None, "msg": None}
        super().__init__()

    @required_login
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.ret['msg']['href'] = reverse('user:login')
            return JsonResponse(self.ret)

        start_obj = request.POST.get('cid', None)
        operate = request.POST.get('type', None)
        user = request.user.id

        ret = Post.handle_point(user=user, operate=operate, model=Post, obj=start_obj)

        self.ret['status'], self.ret['msg'] = ret

        return JsonResponse(self.ret)
