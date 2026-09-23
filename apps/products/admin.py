from django.contrib import admin
from .models import Category, Product, ProductViewHistory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'view_count', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description', 'tags')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ProductViewHistory)
class ProductViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'session_key', 'viewed_at')
    list_filter = ('viewed_at',)
