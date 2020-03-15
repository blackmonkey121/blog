# Register your models here.
import xadmin
from .models import SideBar, Link, Favorite
from apps.blog.base_admin import BaseAdmin


@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')


@xadmin.sites.register(Link)
class LinkAdmin(BaseAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')


@xadmin.sites.register(Favorite)
class FavoriteAdmin(BaseAdmin):
    list_display = ('title', 'href', 'status', 'created_time', 'owner')
    fields = ('title', 'href', 'status')