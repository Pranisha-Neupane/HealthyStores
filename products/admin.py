"""Admin configuration for products — manage the menu from /admin."""
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'featured')
    list_filter = ('category', 'available', 'featured')
    list_editable = ('price', 'available', 'featured')
    search_fields = ('name', 'ingredients')
    prepopulated_fields = {'slug': ('name',)}
