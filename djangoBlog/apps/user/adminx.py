import xadmin
from apps.blog.base_admin import BaseAdmin
from apps.user.models import UserInfo
from xadmin.layout import Row, Fieldset
# Register your models here.


# @xadmin.sites.register(UserInfo)
# class UserAdmin(BaseAdmin):
#     # 定义在详细信息中显示的字段 可以是列表 元组
#     list_display = ('username', 'email','phone', 'is_active', 'avatar', 'nickname')
#
#     # 也可以由fieldsets 字段 来指定
#
#     form_layout = (
#         Fieldset(
#             '必填信息',
#             'username',
#             'password',
#             'email',
#             'phone'
#         ),
#         Fieldset(
#             '选填',
#             Row('nickname','is_active'),
#             'avatar'
#         ),
#     )
