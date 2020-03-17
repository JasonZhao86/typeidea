from django import forms


# 自定义admin页面的Form表单字段
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label="摘要信息", required=False)
