from django import forms

from dal import autocomplete
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from blog.models import Category, Tag, Post


# 自定义admin页面的Form表单字段
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(
        label="摘要信息",
        widget=forms.Textarea,
        required=False
    )
    content_ck = forms.CharField(
        label="正文",
        # widget=CKEditorWidget(),          # 不带图片上传功能的富文本编辑组件
        widget=CKEditorUploadingWidget(),   # 带图片上传功能的富文本编辑组件
        required=False
    )
    content_md = forms.CharField(
        label="正文",
        widget=forms.Textarea(),
        required=False
    )
    content = forms.CharField(
        label="正文",
        widget=forms.HiddenInput(),
        required=False
    )
    category = forms.ModelChoiceField(
        label="分类",
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url="category_autocomplete"),
    )
    tag = forms.ModelMultipleChoiceField(
        label="标签",
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url="tag_autocomplete"),
    )

    class Meta:
        mode = Post
        # 需要把自动补全的字段放到前面
        fields = (
            "category", "tag", "desc", "title",
            "is_md", "content", "content_ck", "content_md",
            "status",
        )

    def __init__(self, instance=None, initial=None, **kwargs):
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial["content_md"] = instance.content
            else:
                initial["content_ck"] = instance.content
        super().__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        is_md = self.cleaned_data.get("is_md")
        if is_md:
            content_field_name = "content_md"
        else:
            content_field_name = "content_ck"
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name, "文章正文为必填项")
        self.cleaned_data["content"] = content
        return super().clean()

    class Media:
        js = ("js/post_editor.js", )
