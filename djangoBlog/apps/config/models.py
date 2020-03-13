from django.db import models

# Create your models here.
from django.template.loader import render_to_string


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    title = models.CharField(max_length=50, verbose_name="标题")
    href = models.URLField(verbose_name="链接")    # default length ：200

    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="状态")
    weight = models.PositiveIntegerField(default=1,
                                         choices=((i, i) for i in range(1,6)),
                                         verbose_name="权重",
                                         help_text="权重越高越靠前")

    owner = models.ForeignKey('user.UserInfo', verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "友链"

    def __repr__(self):
        return 'Link:{}'.format(self.title)


class SideBar(models.Model):

    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMIT = 4
    SIDE_TYPE = (
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, '最新文章'),
        (DISPLAY_HOT, '最热文章'),
        (DISPLAY_COMMIT, '最近评论'),
    )

    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_HIDE,"隐藏"),
        (STATUS_HIDE,"展示")
    )

    title = models.CharField(max_length=50, verbose_name= "标题")
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE, verbose_name="展示类型")
    content = models.CharField(max_length=500, blank=True, verbose_name="内容", help_text="如果不是HTML 可设置为空")
    status = models.PositiveIntegerField(default=STATUS_SHOW, choices=STATUS_ITEMS, verbose_name="状态" ,help_text="展示或隐藏")
    owner = models.ForeignKey('user.UserInfo', verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def content_html(self,user_id):
        """ 直接在models层 渲染模版 """
        # FIXME: 每次查询只需要获取前n条记录！！！ 改写逻辑层切片操作
        # TODO: 直接写SQL查询 需要注意线上数据库的兼容

        from apps.blog.models import Post    # 避免循环引用
        from apps.comment.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content[:5]
        elif self.display_type == self.DISPLAY_LATEST:
            context = {
                'posts': Post.get_latest_article(user_id=user_id)[:5]
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                'posts': Post.get_hot_articles(user_id=user_id)[:5]
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_COMMIT:
            context = {
                'comments': Comment.objects.filter(status=Comment.STATUS_NORMAL, target__owner_id=user_id).select_related('owner', 'target')[:5]
            }
            result = render_to_string('config/blocks/sidebar_comments.html',context)
        return result

    class Meta:
        verbose_name = verbose_name_plural = "侧边栏"

    def __repr__(self):
        return '<SideBar:{}>'.format(self.title)