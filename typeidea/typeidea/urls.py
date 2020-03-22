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
from django.conf.urls import url
from django.contrib import admin

from .custom_site import custom_site
# from blog.views import post_list, post_detail        # function view
from blog.views import (
    IndexView, CategoryView, TagView, PostDetailView, SearchView,
    AuthorView,
)
from config.views import LinkView
from comment.views import CommentView
from typeidea.autocomplete import CategoryAutocomplete, TagAutocomplete

import xadmin


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
    # url(r'^super_admin/', admin.site.urls, name="super_admin"),
    # url(r'^admin/', custom_site.urls, name="admin"),
    url(r'^admin/', xadmin.site.urls, name="xadmin"),
]
