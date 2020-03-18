from django.shortcuts import render
from django.http import HttpResponse
from .models import Tag, Post, Category
from config.models import SideBar


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
