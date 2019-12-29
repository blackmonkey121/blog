from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Post, Tag, Category
from apps.config.models import SideBar, Link
# Create your views here.


class ArticleListView(ListView):
    queryset = Post.get_latest_article()
    paginate_by = 1
    context_object_name = 'article_list'  # 不设置需要在模版中使用 object_list
    template_name = 'blog/article_list.html'


class CommonViewMixmin(object):
    """
    为IndexView 添加通用数据
    """
    def get_context_data(self, **kwargs):
        """ 重写get_context_data 方法 （这个方法属于ListView的父类 MultipleObjectMixin） """
        context = super().get_context_data(**kwargs)    # 多继承 super 会按照MRO列表执行方法
        context.update({
            'sidebars':self.get_sidebars()
        })
        context.update(
            self.get_navs()
        )
        return context

    def get_sidebars(self):
        return SideBar.objects.filter(status=SideBar.STATUS_SHOW)

    def get_navs(self):
        categories = Category.objects.filter(status=Category.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }


class IndexView(CommonViewMixmin, ListView):
    queryset = Post.get_latest_article()
    paginate_by = 3
    context_object_name = "article_list"
    template_name = "blog/article_list.html"


class CategoryView(IndexView):
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
    queryset = Post.get_latest_article()
    template_name = 'blog/article_detail.html'
    context_object_name = "article"
    pk_url_kwarg = "post_id"






@login_required()
def post_list(request,category_id=None, tag_id=None):

    tag = category = None

    # if tag_id:
    #     try:
    #         tag = Tag.objects.get(id=tag_id)
    #     except Tag.DoesNotExist:
    #         article_list = []
    #     else:
    #         article_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    # else:
    #     article_list = Post.objects.filter(status=Post.STATUS_NORMAL)
    #     if category_id:
    #         try:
    #             category = Category.objects.filter(id=category_id)
    #         except Category.DoesNotExist:
    #             category = None
    #         else:
    #             article_list = article_list.filter(category_id=category_id)

    # FIXME: 一样的逻辑，可以抽取 ，封装类时注意

    if tag_id:
        article_list, tag = Post.get_article_tag(tag_id)
    elif category_id:
        article_list, category = Post.get_article_category(category_id)
    else:
        article_list = Post.get_latest_article()

    context = {'category': category,
               'tag': tag,
               'article_list': article_list}

    context.update(Category.get_navs())
    context.update(SideBar.get_sidebars())

    return render(request, 'blog/article_list.html',
                  context=context)
    # return HttpResponse('Anything is OK!')


@login_required()
def post_detail(request, post_id=None):
    try:
        article = Post.objects.filter(id = post_id)
    except Post.DoesNotExist:
        article = None

    context = {
        'article': article
    }
    context.update(Category.get_navs())
    context.update(SideBar.get_sidebars())
    return render(request,'blog/article_detail.html',
                  context=context)
    # return HttpResponse('Anything is OK!')


@login_required()
def links(request):
    return HttpResponse('links:Anything is OK!')


def test(request):
    o = Post.objects.filter(pk=1).first()
    o = o.get_count
    print(o())
    return HttpResponse(str(o()))