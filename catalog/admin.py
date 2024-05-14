from django.contrib import admin

# Register your models here.
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from catalog.models import CatalogItem


# Register your models here.

@admin.register(CatalogItem)
class CatalogItemAdmin(DraggableMPTTAdmin):
    list_display = ("id", 'level', "tree_actions", "indented_title", 'slug', 'parent',)
    list_display_links = ("id", "level", "indented_title",)
