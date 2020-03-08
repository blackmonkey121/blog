# Register your models here.
import xadmin
from django.utils.html import format_html
from apps.blog.base_admin import BaseAdmin
from apps.blog.models import Post
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

    def formfield_for_dbfield(self, db_field, **kwargs):
        """ 过滤外键 """
        if self.request.user.is_superuser:
            if db_field.name == "target":
                kwargs["queryset"] = Post.objects.filter(owner=self.request.user)
        return super().formfield_for_dbfield(db_field, **kwargs)

    operator.short_description = '评论操作'
