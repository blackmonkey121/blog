from django.http import JsonResponse
from django.views.generic import DetailView, ListView, View
from django.urls import reverse
from django.db.models import Q, F
from datetime import date

from .models import Post, Tag, Category
from apps.config.models import SideBar, Link, Favorite
from apps.user.models import UserInfo
from libs.login_tools import required_login

# Create your views here.
from ..comment.models import Comment
from libs.warps import cache, cache_wrap


class CommonViewMixmin(object):
    """
    为IndexView 添加通用数据
    """
    # 获取文章的查询集
    # key: 需要传入右边栏信息的模型名, value: 在上下文中的名字，如果为空 则 为模型名小写+s
    update_context_dict = {
        Category: 'categories',
        Tag: 'tags',
        Link: 'links',
        Favorite: 'favorites'
    }

    @cache_wrap()
    def get_queryset(self, **kwargs):
        return Post.get_latest_article(**kwargs)
    # @cache_wrap()
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

        for model, context_name in self.update_context_dict.items():
            if context_name is None:
                raise KeyError('context_name.values() 中不能存在元素为 None')

            context_name = context_name.strip() or model.__name__.lower() + 's'
            context.update({
                context_name: self.get_update(model=model, owner=owner)
            })

        # add sidebars data
        context.update({
            'sidebars': self.get_sidebars(owner=owner)
        })

        # current visited user id
        context.update({
            'visited_user': owner
        })

        return context

    @staticmethod
    @cache_wrap()
    def get_sidebars(owner):
        sidebars = []
        titles = SideBar.objects.filter(status=SideBar.STATUS_SHOW, owner=owner).select_related('owner')
        for title in titles:
            sidebars.append({'title': title.title, 'html': title.content_html(owner)})
        return sidebars

    @cache_wrap()
    def get_update(self, model, owner=None, relate=True):
        qs = model.objects.filter(status=model.STATUS_NORMAL)
        # TODO:依赖 STATUS.NORMAL 属性, 在模型中做约束，必须提供该属性。

        if owner is not None:
            qs = qs.filter(owner=owner)
        else:
            qs = qs.none()
            return qs

        if relate:
            qs = qs.select_related('owner')
        return qs


class IndexView(CommonViewMixmin, ListView):
    paginate_by = 5

    context_object_name = "article_list"

    template_name = "blog/article_list.html"

    @cache_wrap()
    def get_queryset(self, **kwargs):
        user_id = self.kwargs.get('user_id', None)
        if user_id is not None:
            self.owner = UserInfo.objects.filter(pk=user_id).get()
        return super().get_queryset()


class CategoryView(IndexView):
    """
    分类视图
    """
    @cache_wrap()
    def get_queryset(self):
        """ 重写queryset方法 依据分类来过滤信息 """
        category_id = self.kwargs.get("category_id")
        qs = super().get_queryset()
        try:
            self.owner = qs.first().owner
        except AttributeError:
            self.owner = Category.objects.filter(pk=category_id).first().owner
        return qs.filter(category=category_id)


class TagView(IndexView):
    """"""
    @cache_wrap()
    def get_queryset(self):
        """ 重写queryset方法 依据分类来过滤信息 """
        tag_id = self.kwargs.get("tag_id")
        qs = super().get_queryset()
        try:
            self.owner = qs.first().owner
        except AttributeError:
            self.owner = Tag.objects.filter(pk=tag_id).first().owner

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

    @cache_wrap()
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