#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from dal import autocomplete
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Post, Category, Tag



class PostAdminForm(forms.ModelForm):

    content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=False)
    content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=False)
    content = forms.CharField(widget=forms.HiddenInput(), required=False)

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )

    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签'

    )

    class Meta:
        model = Post
        fields = (
            'category', 'tag', 'desc', 'title',
            'editor_type', 'content', 'content_md', 'content_ck',
            'status'
        )

    def __init__(self, instance=None, initial=None, **kwargs):
        initial = initial or {}
        if instance:
            if instance.editor_type == 1:
                initial['content_ck'] = instance.content
            elif instance.editor_type == 0:
                initial['content_md'] = instance.content
            else:
                raise (ValueError,"未找到对应的文章存储格式{}".format(instance.editor_type))

        super().__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        editor_type = self.cleaned_data.get('editor_type')
        if editor_type:
            content_field_name = 'content_ck'
        else:
            content_field_name = 'content_md'
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name, '必填项！')
            return
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = ('js/admin_post.js', )