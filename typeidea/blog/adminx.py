import xadmin
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager, RelatedFieldListFilter

from django.contrib import admin
from .models import Category, Tag, Post
from django.utils.html import format_html
from django.urls import reverse
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry


class PostInline:
    form_layout = (
        Container(
            Row("title", "desc")
        ),
    )
    extra = 1    # 定义额外内联表单（空的表单，用于新增）的数量为1
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ("name", "status", "is_nav", "created_time", "owner", "post_count")
    fields = ("name", "status", "is_nav")

    # 某个分类下文章总数
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")    # 不让用户直接填作者是谁，这是bug


class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, admin_view, field_path):
        super().__init__(field, request, params, model, admin_view, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list("id", "name")


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ("title", "category", "status", "created_time", "owner", "pv", "uv", "operator")
    list_display_links = ("title",)   # 默认list_display列表中的第一项显示为超链接
    list_filter = ["category", ]
    search_fields = ["title", "category__name"]  # category为对象，通过双下划线访问对象的属性

    """
    fields = (
        ("title", "category"),
        "desc",
        "status", "content", "tag",
    )
    """

    form_layout = [
        Fieldset(
            "基本配置",
            Row("title", "category"),
            "status",
            "tag",
        ),
        Fieldset(
            "内容",
            "desc",
            "content",
        ),
    ]

    # 将多对多字段显示为左右选项卡的形式，而非默认的多选select标签
    filter_horizontal = ("tag", )
    # filter_vertical = ("tag", )

    actions_on_top = True
    # actions_on_bottom = True

    # 编辑页面的保持按钮
    # save_on_top = True

    """
    # 引入静态资源Media配置
    @property
    def media(self):
        # xadmin基于Bootstrap，引入会导致页面样式冲突，这里只做演示
        media = super().media
        media.add_js(["https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js", ])
        media.add_css(["https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ])
        return media
    """

    def operator(self, obj):
        return format_html("<a href='{}'>编辑</a>", reverse("xadmin:blog_post_change", args=(obj.id,)))

    operator.short_description = "操作"


# xadmin自带有log功能
# @xadmin.sites.register(LogEntry)
# class LogEntryAdmin:
#     list_display = ("object_repr", "object_id", "action_flag", "action_time", "user", "change_message", )
