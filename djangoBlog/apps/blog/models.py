from django.db import models
from apps.user.models import UserInfo

# Create your models here.
# 数据处理尽可能的集中在了models层，使得views层逻辑更为简单清晰
# FIXME: 虽然应该将数据处理层独立出来，方便后期的扩展和维护,我觉得就Blog而言 集中在Models这样就够了


class Category(models.Model):
    STATUS_DEFAULT = 2
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DEFAULT, '默认'),
    )
    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="正常")

    owner = models.ForeignKey('user.UserInfo', verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    def __str__(self):
        return '<Category:{}>'.format(self.name)


class Tag(models.Model):
    STATUS_DEFAULT = 2
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DEFAULT, '默认'),
    )
    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="状态")
    owner = models.ForeignKey('user.UserInfo', verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "标签"

    def __str__(self):
        return '<Tag:{}>'.format(self.name)


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文", help_text="正文必须为MarkDown格式")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="状态")
    category = models.ForeignKey(Category, verbose_name="文章分类")
    owner = models.ForeignKey('user.UserInfo', verbose_name="作者")
    tag = models.ForeignKey(Tag, verbose_name='标签')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    # add keys pv nv
    pv = models.PositiveIntegerField(default=1)
    nv = models.PositiveIntegerField(default=1)

    # FIXME: 可以添加过滤条件
    @classmethod
    def get_hot_articles(cls, user_id=None):
        if user_id is not None:
            return cls.objects.filter(status=cls.STATUS_NORMAL, owner_id=user_id).order_by('-pv')
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    @staticmethod
    def get_article_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            article_list = []
        else:
            article_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return article_list, tag

    # FIXME：需要过滤当前用户定义的标签 category = Category.objects.filter(id=category_id, owner=user)  user 需要获取
    @staticmethod
    def get_article_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            article_list = []
        else:
            article_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return article_list, category

    @classmethod
    def get_latest_article(cls, user_id=None):
        if user_id is not None:
            return cls.objects.filter(status=cls.STATUS_NORMAL, owner_id=user_id)
        return cls.objects.filter(status=cls.STATUS_NORMAL)

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ["-id"]   # 按照id降序排列

    def __str__(self):
        return '<Post:{}>'.format(self.title)

