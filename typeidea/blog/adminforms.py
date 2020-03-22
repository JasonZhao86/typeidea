from django import forms

from dal import autocomplete

from blog.models import Category, Tag, Post


# 自定义admin页面的Form表单字段
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(
        label="摘要信息",
        widget=forms.Textarea,
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
        fields = ("category", "tag", "title", "status", "desc", "content")
