from django.contrib import admin
from .models import SideBar, Link
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

import xadmin


@xadmin.sites.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ("title", "href", "status", "weight", "owner", "created_time")
    fields = ("title", "href", "status", "weight")


@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ("title", "display_type", "content", "owner", "created_time")
    fields = ("title", "display_type", "content")
