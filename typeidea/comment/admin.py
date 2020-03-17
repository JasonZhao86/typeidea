from django.contrib import admin
from .models import Comment
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.auth import get_permission_codename


@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ("target", "nickname", "content", "website", "created_time")
    exclude = ("created_time", )

    """
    # ModelAdmin的权限逻辑（重写）
    def has_add_permission(self, request):
        import requests
        opts = self.opts   # opts（options对象）是CommentAdmin的所有属性和方法的集合。
        # print(opts.model_name, opts.app_label)
        codename = get_permission_codename("add", opts)   # perm_codename = add_comment

        # 从自身认证数据库中获取权限
        # return request.user.has_perm("{}.{}".format(opts.app_label, codename))

        # 假设django已经集成了现有的SSO系统，权限的管理在SSO系统上，提供了一个权限查询接口（需要双方
        # 统一用户标识以及权限编码）
        perm_code = "{}.{}".format(opts.app_label, codename)   # perm_codename = comment.add_comment
        PERMISSION_API = "http://permission.sso.com/has_perm?user={}&perm_code={}"
        response = request.get(PERMISSION_API.format(request.user.username, perm_code))
        if response.status_code == 200:
            return True
        else:
            return False
    """
