from django.contrib import admin
from .models import Category, Tag, Post
from django.utils.html import format_html
from django.urls import reverse
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry


# TabularInline(扁平的inline), StackedInline（垂直时的inline）
class PostInline(admin.TabularInline):
    fields = ("title", "desc")
    extra = 1    # 定义额外内联表单（空的表单，用于新增）的数量为1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ("name", "status", "is_nav", "created_time", "owner", "post_count")
    fields = ("name", "status", "is_nav")

    # 某个分类下文章总数
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")    # 不让用户直接填作者是谁，这是bug


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户的category"""
    title = "category过滤"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list("id", "name")

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ("title", "category", "status", "created_time", "owner", "operator")
    list_display_links = ("title",)   # 默认list_display列表中的第一项显示为超链接
    list_filter = [CategoryOwnerFilter, ]
    search_fields = ["title", "category__name"]  # category为对象，通过双下划线访问对象的属性

    """
    fields = (
        ("title", "category"),
        "desc",
        "status", "content", "tag",
    )
    """

    fieldsets = [
        ("基本配置", {
            "description": "基本配置描述信息",
            "fields": ("title", "category", "status"),
        }),
        ("内容", {
            "fields": ("desc", "content"),
        }),
        ("其他配置", {
            # 定义css样式，内置的collapse class显示为折叠，wide class为展开
            "classes": ("wide", ),
            "fields": (
                "tag",
                ("pv", "uv"),
            )
        })
    ]

    # 将多对多字段显示为左右选项卡的形式，而非默认的多选select标签
    filter_horizontal = ("tag", )
    # filter_vertical = ("tag", )

    actions_on_top = True
    # actions_on_bottom = True

    # 编辑页面的保持按钮
    # save_on_top = True

    class Media:
        # 引入外部的css和js供fieldsets中的classes使用。
        css = {
            "all": ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        }
        js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js", )

    def operator(self, obj):
        return format_html("<a href='{}'>编辑</a>", reverse("custom_admin:blog_post_change", args=(obj.id,)))

    operator.short_description = "操作"


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("object_repr", "object_id", "action_flag", "action_time", "user", "change_message", )
