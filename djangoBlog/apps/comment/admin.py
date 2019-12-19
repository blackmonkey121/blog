from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from django.urls import reverse
from ..blog.branch_site import branch_site
from .models import Comment


@admin.register(Comment,site=branch_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')

    def operator(self, obj):
        """

        :param obj: 当前对象
        """
        from django.urls import reverse
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_comment_change', args=(obj.id,))
        )

    operator.short_description = '评论操作'
