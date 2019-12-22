from django.contrib import admin
from apps.user.models import UserInfo
from apps.blog.branch_site import branch_site
# Register your models here.


@admin.register(UserInfo, site=branch_site)
class UserAdmin(admin.ModelAdmin):
    # 定义在详细信息中显示的字段 可以是列表 元组
    list_display = ('username', 'email','phone', 'is_active', 'avatar', 'nickname')

    # 也可以由fieldsets 字段 来指定
    fieldsets = (
        ('必填信息', {'fields': ('username','password', 'email')}),
        ('选填信息', {'fields': ('phone', 'avatar', 'nickname', 'is_active')}),
    )

