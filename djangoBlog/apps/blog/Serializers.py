#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from rest_framework import serializers, pagination

from .models import Post, Category, Tag


class ArticleSerializer(serializers.HyperlinkedModelSerializer):

    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    tag = serializers.SlugRelatedField(
        many= True,
        read_only=True,
        slug_field='name',
    )

    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    created_time = serializers.DateTimeField(format='%Y-%m-%d %H%M%S')

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'created_time', 'owner', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api_article_detail'}
        }


class ArticleDetailSerializer(ArticleSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'content_html', 'owner', 'created_time']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time', 'url']


class CategoryDetailSerializer(CategorySerializer):
    articles = serializers.SerializerMethodField('paginated_articles')

    def paginated_articles(self, obj):
        articles = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(articles, self.context['request'])
        serializer = ArticleSerializer(page, many=True, context={
            'request':self.context['request']
        })
        return {
            'count': articles.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time', 'articles', 'url']
