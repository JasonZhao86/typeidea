from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_title = "Typeidea后台管理"
    site_header = "Typeidea"
    index_title = "首页"


# name定义该admin站点的namespace，reverse反向解析是引用该名称
custom_site = CustomSite(name="custom_admin")
