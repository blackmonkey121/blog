from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.generic import DetailView, ListView, View
from django.core.urlresolvers import reverse

from .models import Post, Tag, Category
from apps.config.models import SideBar
from apps.user.models import UserInfo
from django.db.models import Q, F
from datetime import date

# Create your views here.
from ..comment.models import Comment
from libs.warps import cache, cache_warp


class CommonViewMixmin(object):
    """
    为IndexView 添加通用数据
    """
    # 获取文章的查询集
    @cache_warp()
    def get_queryset(self, **kwargs):
        return Post.get_latest_article(**kwargs)

    def get_context_data(self, **kwargs):
        """
        重写get_context_data 方法 （这个方法属于ListView的父类 MultipleObjectMixin）
        添加侧边栏数据 和 其它附加数据集
        """
        if hasattr(self, 'owner'):
            owner = self.owner
        else:
            owner = None

        context = super().get_context_data(**kwargs)  # 多继承 super 会按照MRO列表执行方法

        # add sidebars data
        context.update({
            'sidebars': self.get_sidebars(owner=owner)
        })

        # add categories
        context.update({
            'categories': self.get_categories(owner=owner)
        })

        # add tags
        context.update({
            'tags': self.get_tags(owner=owner)
        })

        # current visited user id
        context.update({
            'visited_user': owner
        })

        return context

    @staticmethod
    @cache_warp()
    def get_sidebars(owner):
        sidebars = []
        titles = SideBar.objects.filter(status=SideBar.STATUS_SHOW, owner=owner).select_related('owner')
        for title in titles:
            sidebars.append({'title': title.title, 'html': title.content_html(owner)})
        return sidebars

    @staticmethod
    @cache_warp()
    def get_categories(owner):
        if owner is not None:
            return Category.objects.filter(status=Category.STATUS_NORMAL, owner=owner).select_related('owner')
        return Category.objects.filter(status=Category.STATUS_DEFAULT)

    @staticmethod
    @cache_warp()
    def get_tags(owner):
        if owner is not None:
            return Tag.objects.filter(status=Tag.STATUS_NORMAL, owner=owner).select_related('owner')
        return Tag.objects.filter(status=Tag.STATUS_DEFAULT)


class IndexView(CommonViewMixmin, ListView):
    paginate_by = 5

    context_object_name = "article_list"

    template_name = "blog/article_list.html"

    @cache_warp()
    def get_queryset(self, **kwargs):
        user_id = self.kwargs.get('user_id', None)
        if user_id is not None:
            self.owner = UserInfo.objects.filter(pk=user_id).get()
        return super().get_queryset()


class CategoryView(IndexView):
    """
    分类视图
    """
    @cache_warp()
    def get_queryset(self):
        """ 重写queryset方法 依据分类来过滤信息 """
        category_id = self.kwargs.get("category_id")
        qs = super().get_queryset()
        self.owner = qs.first().owner
        return qs.filter(category=category_id)


class TagView(IndexView):
    """"""
    @cache_warp()
    def get_queryset(self):
        """ 重写queryset方法 依据分类来过滤信息 """
        tag_id = self.kwargs.get("tag_id")
        qs = super().get_queryset()
        self.owner = qs.first().owner

        return qs.filter(tag=tag_id)


class SearchView(IndexView):
    """
    整站搜索
    #TODO：使用全文检索框架 haystack
    """

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


class ArticleDetailView(CommonViewMixmin, DetailView):
    template_name = 'blog/article_detail.html'
    context_object_name = "article"
    pk_url_kwarg = "post_id"

    @cache_warp()
    def get_object(self, queryset=None):
        """ 优化查询 加载外键字段 """
        post_id = self.kwargs.get('post_id')
        obj = Post.objects.filter(pk=post_id).select_related('category', 'owner').get()
        self.owner = obj.owner
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
        article_id = self.kwargs.get("post_id")
        context.update({
            'comments': Comment.objects.filter(target=article_id).order_by('-id').select_related('owner'),
        })
        return context


class UpArticleView(View):

    def __init__(self):
        self.ret = {"status": None, "msg": None}
        super().__init__()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            self.ret['msg']['href'] = reverse('user:login')
            return JsonResponse(self.ret)

        start_obj = request.POST.get('cid', None)
        operate = request.POST.get('type', None)
        user = request.user.id

        ret = Post.handle_point(user=user, operate=operate, model=Post, obj=start_obj)

        self.ret['status'], self.ret['msg'] = ret

        return JsonResponse(self.ret)

@login_required()
def links(request):
    return HttpResponse('links:Anything is OK!')
