import xadmin
from xadmin.filters import RelatedFieldListFilter, manager
from xadmin.layout import Row, Fieldset, Container

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Category, Post, Tag
from apps.user.models import  UserInfo
from .base_admin import BaseAdmin
from .adminforms import PostAdminForm


admin.AdminSite.site_header = 'MonkeyBlog(管理员:{})'.format(admin.AdminSite.urls)
admin.AdminSite.site_title = 'MonkeyBlog(管理员:{})'
admin.AdminSite.index_title = '管理员首页'


class PostInline(object):
    form_layout = (
        Container(
            Row("title", "desc"),
        )
    )
    extra = 1  # 控制额外多几个
    model = Post

# 自定义过滤器
class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        """
        确认字段是否需要被当前过滤器处理
        """
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')

    # title: str = '分类过滤器'
    # parameter_name: str = 'id'
    #
    # def lookups(self, request, model_admin):
    #     return Category.objects.filter(owner=request.user).values_list('id', 'name')
    #
    # def queryset(self, request, queryset):
    #     category_id = self.value()
    #     if category_id:
    #         return queryset.filter(category_id=self.value())
    #     return queryset

    # admin  <flag:note>
    # 定义过滤器只展示当前用户的分类
    # 提供了两个属性
    #     :param title : 用来展示标题
    #     :param queryset :查询时URL的参数名字
    #     eg: 当查询为id为1的分类时URL为 ?owner_category = 1
    # 方法:
    #     lookups:
    #     返回要查询的内容和用到的ID
    #     queryset:
    #     根据 URL Query的内容返回数据 例如 URL Query为 ?owner_category = 1
    #     那么 self.value() 拿到的就是 1

manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Category)
class CategoryAdmin(BaseAdmin):
    # 定义在详细信息中显示的字段 可以是列表 元组
    list_display = ('name', 'created_time', 'owner', 'status', 'post_count')

    # 也可以由fieldsets 字段 来指定
    fields = ('name', 'status')

    # 在 分类页面展示 行内编辑区 PostInline 在上方定义
    inlines = (PostInline,)

    def post_count(self, obj):
        """ 文章数目的统计 """
        return obj.post_set.count()

    # 指定在展示页面 表头信息
    post_count.short_description = "文章数量"


@xadmin.sites.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')


@xadmin.sites.register(Post)
class PostAdmin(BaseAdmin):
    # 后端管理页面的渲染会按照模型表定义的来生成HTML元素 这是给予ModelAdmin和ModelForm的
    # 写一个我们自己的form，指定给ModelAdmin就OK了
    # form字段  PostAdminForm 在 adminforms.py 中
    form = PostAdminForm

    list_display = ('title', 'category', 'created_time',
                    'status', 'operator')

    list_display_links = ['title', 'category']  # 在展示的字段上 添加的超链接

    list_filter = ['category']  # 过滤字段

    search_fields = ['title', 'category__name']  # 检索的字段

    actions_on_top = True  # 动作相关是否在顶部展示
    actions_on_bottom = True  # 动作相关是否在底部展示

    # 编辑页面
    # save_on_top = True      # 保存、编辑、编辑并新建 按钮是否在顶部展示

    # fields： 限制新建 时需要写入的字段  配置真是字段的顺序
    # fields = (
    #     ('category', 'title'),   # 括号括起来 表示在一行展示
    #     'desc',
    #     'content',
    #     ('tag', 'status')
    # )

    # 用来控制 详细的布局：
    # fieldsets = (
    # (名称, {内容}),
    # (名称, {内容}),
    # )

    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'editor_type',
            'content',
            'content_ck',
            'content_md',
        ),
    )

    def get_media(self):
        """
        引入静态资源，这种写法和 改写元类Media的效果是一样的，最终都会转化为 forms.widgets.Media 对象
        :return:
        """
        media = super().get_media()
        media.add_js([
            # 'https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'
        ])
        media.add_css(
            {
                # 'all': ('https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap-grid.css',),
            })
        return media

    def operator(self, obj):
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def queryset(self):
        """ 函数作用：使当前登录的用户只能看到自己的文章和分类等 """
        qs = super().queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(area_company=PostAdmin.objects.get(user=self.request.user))

    def formfield_for_dbfield(self, db_field, **kwargs):
        """ 过滤外键 """
        if self.request.user.is_superuser:
            if db_field.name == "category":
                kwargs["queryset"] = Category.objects.filter(owner=self.request.user)
            if db_field.name == 'tag':
                kwargs['queryset'] = Tag.objects.filter(owner=self.request.user)
        return super().formfield_for_dbfield(db_field, **kwargs)

    # 添加自定义的js 和 CSS
    # class Media:
    #     css = {
    #         'all': ('https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap-grid.css',),
    #     }
    #     js = ('https://cdn.bootcss.com/jquery/3.4.1/core.js',)
