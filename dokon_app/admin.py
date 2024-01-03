from django.contrib import admin
from .models import ProductType, Product, ProductHistorySoldOut, HistorySoldOut, HistoryCame, ProductHistoryCame

admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(ProductHistorySoldOut)
admin.site.register(HistorySoldOut)
admin.site.register(HistoryCame)
admin.site.register(ProductHistoryCame)