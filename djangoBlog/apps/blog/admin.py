from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Post, Tag
from .branch_site import branch_site
from .base_admin import BaseAdmin
from .adminforms import PostAdminForm


admin.AdminSite.site_header = 'djangoBlog(管理员:{})'.format(admin.AdminSite.urls)
admin.AdminSite.site_title = 'djangoBlog(管理员:{})'
admin.AdminSite.index_title = '管理员首页'

# TODO SSO
# TODO 抽取Admin基类 base_admin.py

# class PostInline(admin.StackedInline):   # admin.StackedInline
class PostInline(admin.TabularInline):  # StackedInline 样式不同  也可以继承 admin.StackedInline
    fields = ('title', 'desc')
    extra = 1  # 表示 编辑框的个数
    model = Post  # 指定是那个model


# 自定义过滤器
class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    定义过滤器只展示当前用户的分类
    提供了两个属性
        :param title : 用来展示标题
        :param queryset :查询时URL的参数名字
        eg: 当查询为id为1的分类时URL为 ?owner_category = 1
    方法:
        lookups:
        返回要查询的内容和用到的ID
        queryset:
        根据 URL Query的内容返回数据 例如 URL Query为 ?owner_category = 1
        那么 self.value() 拿到的就是 1
    """
    title: str = '分类过滤器'
    parameter_name: str = 'id'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


# site = branch_site 分支站点展示用来分割权限
@admin.register(Category, site=branch_site)
class CategoryAdmin(BaseAdmin):
    # 定义在详细信息中显示的字段 可以是列表 元组
    list_display = ('name', 'is_nav', 'created_time', 'owner', 'status', 'post_count')

    # 也可以由fieldsets 字段 来指定
    fields = ('name', 'status', 'is_nav')

    # 在 分类页面展示 行内编辑区 PostInline 在上方定义
    inlines = (PostInline,)

    def post_count(self, obj):
        """ 文章数目的统计 """
        return obj.post_set.count()

    # 指定在展示页面 表头信息
    post_count.short_description = "文章数量"


@admin.register(Tag, site=branch_site)
class TagAdmin(BaseAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


@admin.register(Post, site=branch_site)
class PostAdmin(BaseAdmin):
    # 后端管理页面的渲染会按照模型表定义的来生成HTML元素 这是给予ModelAdmin和ModelForm的
    # 写一个我们自己的form，指定给ModelAdmin就OK了
    # form字段  PostAdminForm 在 adminforms.py 中
    form = PostAdminForm

    list_display = ('title', 'category', 'created_time',
                    'status', 'operator')

    list_display_links = ['title', 'category']  # 在展示的字段上 添加的超链接

    list_filter = [CategoryOwnerFilter]  # 过滤字段

    search_fields = ['title', 'category__name']  # 检索的字段

    actions_on_top = True  # 动作相关是否在顶部展示
    actions_on_bottom = False  # 动作相关是否在底部展示

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

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
            ),
        }
         ),
        ('内容', {
            'description': '文章内容',
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': (('tag', 'status'),),
        })
    )

    # filter_horizontal = ('tag',)
    # filter_vertical = ('tag',)

    def operator(self, obj):
        """
        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('branch_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    # 添加自定义的js 和 CSS
    class Media:
        css = {
            'all': ('https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap-grid.css',),
        }
        js = ('https://cdn.bootcss.com/jquery/3.4.1/core.js',)


# 日志
@admin.register(LogEntry, site=branch_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']