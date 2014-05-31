from django.contrib import admin
from .models import Product,ProductBrand,ProductCategory

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','is_active','bar_code','inventory','unit_price','category','brand']

# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductBrand)
