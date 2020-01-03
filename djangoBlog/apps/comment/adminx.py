# Register your models here.
import xadmin
from django.utils.html import format_html
from apps.blog.base_admin import BaseAdmin
from django.urls import reverse
from .models import Comment


@xadmin.sites.register(Comment)
class CommentAdmin(BaseAdmin):
    list_display = ('target', 'nickname', 'content', 'owner', 'created_time')

    def operator(self, obj):
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_comment_change', args=(obj.id,))
        )

    operator.short_description = '评论操作'
