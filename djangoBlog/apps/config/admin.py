from django.contrib import admin

# Register your models here.

from .models import SideBar, Link


@admin.register(SideBar)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.ower = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

    def save_model(self, request, obj, form, change):
        obj.ower = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)
