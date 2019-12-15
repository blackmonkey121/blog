from django.db import models
from ..blog.models import Post


# Create your models here.


class Comment(models.Model):
    """
    评论表
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    target = models.ForeignKey(Post,verbose_name='评论对象')
    content = models.CharField(max_length=2048, verbose_name="内容")
    nickname = models.CharField(max_length=32, verbose_name="用户名")
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "评论"

    def __repr__(self):
        return '<Comment:{}>'.format(self.content)
