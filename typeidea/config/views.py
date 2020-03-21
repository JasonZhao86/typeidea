from django.shortcuts import render
from django.views.generic import ListView

from blog.views import CommonViewMixin
from .models import Link


class LinkView(CommonViewMixin, ListView):
    queryset = Link.get_all()
    context_object_name = "link_list"
    template_name = "config/links.html"
