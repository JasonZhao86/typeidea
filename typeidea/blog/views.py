from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Tag, Post, Category
from config.models import SideBar


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "sidebars": SideBar.get_all()
        })
        context.update(Category.get_nav())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.get_lastest_post()
    context_object_name = "post_list"
    template_name = "blog/list.html"
    paginate_by = 1


class CategoryView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get("category_id", 1)
        return queryset.filter(category__id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id", 1)
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            "category": category,
        })
        return context


class TagView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get("tag_id", 1)
        return queryset.filter(tag__id=tag_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get("tag_id", 1)
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            "tag": tag,
        })
        return context


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.get_lastest_post()
    pk_url_kwarg = "post_id"
    context_object_name = "post"
    template_name = "blog/detail.html"


"""
# function view，其中IndexView、CategoryView和TagView均是从post_list中拆出来的。
def post_list(request, category_id=None, tag_id=None):
    category = None
    tag = None
    if tag_id:
        tag, post_list = Post.get_post_by_tag(tag_id)
    elif category_id:
        category, post_list = Post.get_post_by_category(category_id)
    else:
        post_list = Post.get_lastest_post()
    context = {
        "category": category,
        "tag": tag,
        "post_list": post_list,
        "sidebars": SideBar.get_all(),
    }
    context.update(Category.get_nav())
    return render(request, "blog/list.html", context=context)


def post_detail(request, post_id):
    post = Post.get_post_by_id(post_id)
    context = {"post": post, "sidebars": SideBar.get_all()}
    context.update(Category.get_nav())
    return render(request, "blog/detail.html", context=context)
"""
