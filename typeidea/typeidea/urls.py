"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import xadmin
import ckeditor_uploader
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from .custom_site import custom_site
# from blog.views import post_list, post_detail        # function view
from blog.views import (
    IndexView, CategoryView, TagView, PostDetailView, SearchView,
    AuthorView,
)
from config.views import LinkView
from comment.views import CommentView
from typeidea.autocomplete import CategoryAutocomplete, TagAutocomplete
# from blog.apis import post_list, PostList
from blog.apis import PostViewSet, CategoryViewSet, TagViewSet


router = DefaultRouter()
# 这里的basename就类似于名称空间，即url reverse的前缀。
router.register(r'post', PostViewSet, basename="api-post")
router.register(r'category', CategoryViewSet, basename="api-category")
router.register(r'tag', TagViewSet, basename="api-tag")


urlpatterns = [
    url(r'^$', IndexView.as_view(), name="post_list"),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name="post_list_by_category"),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name="post_list_by_tag"),
    url(r'^author/(?P<author_id>\d+)/$', AuthorView.as_view(), name="post_list_by_author"),
    url(r'^post/(?P<post_id>\d+).html/$', PostDetailView.as_view(), name="post_detail"),
    url(r'^keyword/$', SearchView.as_view(), name="search"),
    url(r'^links/$', LinkView.as_view(), name="links"),
    url(r'^comment/$', CommentView.as_view(), name="comment"),
    url(r'^category_autocomplete/$', CategoryAutocomplete.as_view(), name="category_autocomplete"),
    url(r'^tag_autocomplete/$', TagAutocomplete.as_view(), name="tag_autocomplete"),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),   # ckeditor保存和浏览上传的图片的两个接口
    # url(r'^api/posts/$', post_list, name="post_list"),
    # url(r'^api/posts/$', PostList.as_view(), name="post_list"),
    url(r'^api/', include(router.urls, namespace="api")),    # namespace和self.reverse_action不能同用
    url(r'^api/docs/', include_docs_urls(title="Typeidea api docs")),
    # url(r'^super_admin/', admin.site.urls, name="super_admin"),
    # url(r'^admin/', custom_site.urls, name="admin"),
    url(r'^admin/', xadmin.site.urls, name="xadmin"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
