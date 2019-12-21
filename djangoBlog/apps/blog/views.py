from django.shortcuts import render,redirect,HttpResponse
from .models import Post, Tag, Category
from apps.config.models import SideBar, Link
# Create your views here.


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
        article_list, category = Post.get_article_tag(category_id)
    else:
        article_list = Post.get_latest_article()

    context = {'category': category,
               'tag': tag,
               'article_list': article_list}

    context.update(Category.get_navs())
    context.update(SideBar.get_sidebars())

    return render(request, 'blog/article.html',
                  context=context)
    # return HttpResponse('Anything is OK!')


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


def links(request):
    return HttpResponse('links:Anything is OK!')