from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label="昵称",
        max_length=50,
        widget=forms.widgets.Input(attrs={"class": "form-control", "style": "width: 60%"})
    )
    website = forms.CharField(
        label="网址",
        max_length="100",
        widget=forms.widgets.URLInput(attrs={"class": "form-control", "style": "width: 60%"})
    )
    email = forms.EmailField(
        label="邮箱",
        max_length="50",
        widget=forms.widgets.EmailInput(attrs={"class": "form-control", "style": "width: 60%"})
    )
    content = forms.CharField(
        label="内容",
        max_length="500",
        widget=forms.widgets.Textarea(attrs={"class": "form-control", "style": "rows: 6; cols:60;"})
    )

    def clean_content(self):
        # form表单中有content这个input标签，所以一定有content这个key
        content = self.cleaned_data.get("content")
        if len(content) < 10:
            raise forms.ValidationError("评论数量不能低于10个字符！")
        return content

    class Meta:
        model = Comment
        fields = ["nickname", "email", "website", "content"]
