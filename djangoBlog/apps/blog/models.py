from django.db import models
from django.utils.functional import cached_property
import mistune
from django.utils.html import mark_safe

from apps.user.models import UserInfo

# Create your models here.
# 数据处理尽可能的集中在了models层，使得views层逻辑更为简单清晰

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
        ordering=['-id']

    def __str__(self):
        return self.name


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
        ordering = ['-id']

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    TYPE_MARKDOWN = 0
    TYPE_CKEDITOR = 1
    EDITOR_TYPE_ITEMS = (
        (TYPE_MARKDOWN, 'markdown编辑器'),
        (TYPE_CKEDITOR, '常规编辑器'),
    )

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文", help_text="MarkDown格式")
    content_html = models.TextField(verbose_name="正文html", blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="状态")
    category = models.ForeignKey(Category, verbose_name="文章分类")
    owner = models.ForeignKey('user.UserInfo', verbose_name="作者")
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    # add keys pv nv
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    editor_type = models.PositiveIntegerField(choices=EDITOR_TYPE_ITEMS, default=TYPE_CKEDITOR, verbose_name='编辑器类型')

    @classmethod
    def get_hot_articles(cls, user_id=None, related=True):
        qs = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

        if user_id is not None:
            qs = qs.filter(owner=user_id)
            # qs = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
        if related:
            qs = qs.select_related('owner', 'category')
            # return cls.objects.filter(status=cls.STATUS_NORMAL, owner_id=user_id).order_by('-pv')
        # return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
        return qs

    @staticmethod
    def get_tag_article(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            article_list = []
        else:
            article_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return article_list, tag

    @staticmethod
    def get_category_article(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            article_list = []
        else:
            article_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return article_list, category

    @classmethod
    def get_latest_article(cls, user_id=None, related=True):
        if user_id is not None:
            return cls.objects.filter(status=cls.STATUS_NORMAL, owner_id=user_id).select_related('owner', 'category')
        qs = cls.objects.filter(status=cls.STATUS_NORMAL)

        if related:
            qs.select_related('owner', 'category')

        return qs

    def save(self, *args, **kwargs):
        """ 重写文章主体 """
        safe_content = mark_safe(self.content)
        if self.editor_type:
            # ckeditor 转换出 的就是html格式
            self.content_html = safe_content
        else:
            self.content_html = mistune.markdown(safe_content)
        super().save(*args, **kwargs)

    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ["-id"]   # 按照id降序排列

    def __str__(self):
        return self.title

