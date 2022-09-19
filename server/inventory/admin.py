from django.contrib import admin

from inventory.models import Brand, Category, Inventory, Product, ProductAttribute, ProductImage, StockControl

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass

@admin.register(StockControl)
class StockControlAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",),
    }


class ProductAttributeAdmin(admin.TabularInline):
    model = ProductAttribute


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, StockControlAdmin]

