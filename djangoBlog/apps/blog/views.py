from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Post, Tag, Category
from apps.config.models import SideBar, Link
from apps.user.models import UserInfo
from django.db.models import Q, F
from datetime import date
from django.core.cache import cache

# Create your views here.
from ..comment.models import Comment


class CommonViewMixmin(object):
    """
    为IndexView 添加通用数据
    """

    def get_current_user_id(self: object) -> object:

        user_id = self.kwargs.get('user_id')
        if user_id:
            return user_id

        post_id = self.kwargs.get('post_id')
        if post_id:
            return Post.objects.filter(id=post_id).first().owner.id

        tag_id = self.kwargs.get('tag_id')
        if tag_id:
            return Tag.objects.filter(id=tag_id).first().owner.id

        category_id = self.kwargs.get('category_id')
        if category_id:
            return Category.objects.filter(id=category_id).first().owner.id

    # 获取查询集文章

    def get_queryset(self):

        user_id = self.get_current_user_id()

        if user_id:
            return Post.get_latest_article(user_id=user_id)
        else:
            return Post.get_latest_article()

    def get_context_data(self, **kwargs):
        """
        重写get_context_data 方法 （这个方法属于ListView的父类 MultipleObjectMixin）
        添加侧边栏数据 和 其它附加数据集
        """
        # get visited user id
        user_id = self.get_current_user_id()
        context = super().get_context_data(**kwargs)  # 多继承 super 会按照MRO列表执行方法

        # add sidebars data
        context.update({
            'sidebars': self.get_sidebars(owner_id=user_id)
        })

        # add categories
        context.update({
            'categories': self.get_categories(owner_id=user_id)
        })

        # add tags
        context.update({
            'tags': self.get_tags(owner_id=user_id)
        })

        # current visited user id
        context.update({
            'visited_user': UserInfo.objects.filter(id=user_id).first()
        })

        return context

    @staticmethod
    def get_sidebars(owner_id: int = None):
        sidebars = []
        titles = SideBar.objects.filter(status=SideBar.STATUS_SHOW, owner_id=owner_id).select_related('owner')
        for title in titles:
            sidebars.append({'title': title.title, 'html': title.content_html(owner_id)})
        return sidebars

    @staticmethod
    def get_categories(owner_id: int = None):
        if owner_id is not None:
            return Category.objects.filter(status=Category.STATUS_NORMAL, owner_id=owner_id).select_related('owner')
        return Category.objects.filter(status=Category.STATUS_DEFAULT)

    @staticmethod
    def get_tags(owner_id: int = None):
        if owner_id is not None:
            return Tag.objects.filter(status=Tag.STATUS_NORMAL, owner_id=owner_id).select_related('owner')
        return Tag.objects.filter(status=Tag.STATUS_DEFAULT)


class IndexView(CommonViewMixmin, ListView):
    paginate_by = 5

    context_object_name = "article_list"

    template_name = "blog/article_list.html"

    def get_context_data(self, **kwargs):
        con = super().get_context_data()
        print(self)
        return con


class CategoryView(IndexView):

    def get_context_data(self, **kwargs):
        """ 重写get_context_data 方法 产生期望的数据集 """
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)  # 获取一个对象的实例 else rasie 404
        context.update({
            'category': category,
        })
        print(context)
        return context

    def get_queryset(self):
        """ 重写queryset方法 依据分类来过滤信息 """
        queryset = super().get_queryset()
        category_id = self.kwargs.get("category_id")
        return queryset.filter(category_id=category_id)


class TagView(IndexView):

    def get_context_data(self, **kwargs):
        """ 重写get_context_data 方法 产生期望的数据集 """
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)  # 获取一个对象的实例 else rasie 404
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """ 重写queryset方法 依据标签来过滤信息 """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get("tag_id")
        tag = Tag.objects.filter(id=tag_id).first()
        return queryset.filter(tag=tag)


class SearchView(IndexView):
    """
    整站搜索
    #TODO：使用全文检索框架 haystack
    """

    def get_queryset(self):
        query_set = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        # keyword = self.args.get('keyword')
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

    def get_object(self, queryset=None):
        """ 优化查询 加载外键字段 """
        post_id = self.kwargs.get('post_id')
        obj = Post.objects.filter(pk=post_id).select_related('category', 'owner').get()
        return obj

    def get(self, request, *args, **kwargs):
        # FIXME: 内存做缓存，单进程是可以的，但是多进程会使得 进程数据不安全 进程之间内存是相互独立的。
        # TODO: 改为 Redis 做缓存  使用Celery 来异步的处理访问计数的功能

        response = super().get(request, *args, **kwargs)
        self.handle_visited(request)
        return response

    def handle_visited(self, request):
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
            cache.set(pv_key, 1, 24 * 60 * 60)
        print(self.object)

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
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
        print(context)
        return context


@login_required()
def links(request):
    return HttpResponse('links:Anything is OK!')
