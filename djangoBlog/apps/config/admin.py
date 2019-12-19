from django.contrib import admin

# Register your models here.

from .models import SideBar, Link
from ..blog.branch_site import branch_site
from ..blog.base_admin import BaseAdmin


@admin.register(SideBar, site=branch_site)
class SideBarAdmin(BaseAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')


@admin.register(Link, site=branch_site)
class LinkAdmin(BaseAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

