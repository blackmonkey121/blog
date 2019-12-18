from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Post, Tag
from .branch_site import branch_site

# TODO SSO


class PostInline(admin.TabularInline):   # StackedInline 样式不用
    fields = ('title', 'desc')
    extra = 1
    model = Post


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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_nav', 'created_time', 'owner', 'status', 'post_count')
    # 定义在详细信息中显示的字段 可以是列表 元组

    fields = ('name', 'status', 'is_nav')

    inlines = [PostInline,]

    # 新增记录时需要写入的信息

    def save_model(self, request, obj, form, change):
        """
        指定作者只能是当前登陆用户而不能是其他人
        :param request: 当前的请求对象
        :param obj: 当前要保存的对象
        :param form: 页面提交过来的表单对象
        :param change: 保存本次的数据是新增的还是更新的
        """
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"

    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(TagAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


@admin.register(Post,site=branch_site)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_time', 'status', 'operator', 'post_count')

    list_display_links = ['title', 'category']  # 在展示的字段上 添加的超链接
    list_filter = [CategoryOwnerFilter]      # 过滤字段
    search_fields = ['title', 'category__name']   # 检索的字段

    actions_on_top = True    # 动作相关是否在顶部展示
    actions_on_bottom = False   # 动作相关是否在底部展示

    # 编辑页面
    # save_on_top = True      # 保存、编辑、编辑并新建 按钮是否在顶部展示

    exclude = ('owner',)

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
        ('基础配置',{
            'description': '基础配置描述',
            'fields': (
                ('title','category'),
            ),
        }
    ),
        ('内容',{
            'description': '文章内容',
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息',{
            'classes': ('collapse',),
            'fields': (('tag','status'),),
        })
    )

    # filter_horizontal = ('tags',)
    # filter_vertical = ('tags',)

    def operator(self, obj):
        """

        :param obj: 当前对象
        """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('branch_admin:blog_post_change',args=(obj.id,))
                           )
    operator.short_description = '操作'
    def post_count(self, obj):
        """
        :param obj: 当前对象
        """

    post_count.short_description = '总数'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin,self).get_queryset(request)
        return qs.filter(owner = request.user)


    # 添加自定义的js 和 CSS
    class Media:
        css = {
            'all':('https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap-grid.css',),
        }
        js = ('https://cdn.bootcss.com/jquery/3.4.1/core.js',)
