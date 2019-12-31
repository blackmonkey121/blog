from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Post, Tag, Category
from apps.config.models import SideBar, Link
from apps.user.models import UserInfo
# Create your views here.


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
    # queryset = Post.get_latest_article()

    def get_queryset(self, **kwargs):

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
        context = super().get_context_data(**kwargs)    # 多继承 super 会按照MRO列表执行方法

        # add sidebars data
        context.update({
            'sidebars':self.get_sidebars(owner_id=user_id)
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
        titles = SideBar.objects.filter(status=SideBar.STATUS_SHOW, owner_id=owner_id)
        for title in titles:
            sidebars.append({'title': title.title,'html':title.content_html(owner_id)})
        return sidebars

    @staticmethod
    def get_categories(owner_id: int = None):
        if owner_id is not None:
            return Category.objects.filter(status=Category.STATUS_NORMAL, owner_id=owner_id)
        return Category.objects.filter(status=Category.STATUS_DEFAULT)

    @staticmethod
    def get_tags(owner_id: int = None):
        if owner_id is not None:
            return Tag.objects.filter(status=Tag.STATUS_NORMAL, owner_id=owner_id)
        return Tag.objects.filter(status=Tag.STATUS_DEFAULT)


class IndexView(CommonViewMixmin, ListView):
    paginate_by = 5
    context_object_name = "article_list"
    template_name = "blog/article_list.html"


class CategoryView(IndexView):

    # def get_queryset(self,**kwargs):
    #     category_id = self.kwargs.get('category_id')
    #     query_set= super().get_queryset()
    #     if category_id:
    #         return query_set.filter(id=category_id)

    def get_context_data(self, **kwargs):
        """ 重写get_context_data 方法 产生期望的数据集 """
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)    #获取一个对象的实例 else rasie 404
        context.update({
            'category': category,
        })
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
        tag = get_object_or_404(Tag, pk=tag_id)    #获取一个对象的实例 else rasie 404
        context.update({
            'tag':tag,
        })
        return context

    def get_queryset(self):
        """ 重写queryset方法 依据标签来过滤信息 """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get("tag_id")
        return queryset.filter(tag_id=tag_id)


class ArticleDetailView(CommonViewMixmin, DetailView):

    template_name = 'blog/article_detail.html'
    context_object_name = "article"
    pk_url_kwarg = "post_id"


@login_required()
def links(request):
    return HttpResponse('links:Anything is OK!')