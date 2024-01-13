from django.contrib import admin
from .models import (
    HistorySoldOut,
    HistoryCame,
    HistoryObject,
    ObjectPayment,
    DokonDay,
    Product,
    ProductHistoryCame,
    ProductHistoryObject,
    ProductHistorySoldOut,
    ProductType,
)

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_type', 'name', 'date')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'name', 'price', 'profit_percentage', 'remain', 'date')

@admin.register(ProductHistorySoldOut)
class ProductHistorySoldOutAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'number', 'total_amount', 'profit', 'date')

@admin.register(HistorySoldOut)
class HistorySoldOutAdmin(admin.ModelAdmin):
    list_display = ('id', 'responsible', 'total_number_sold_out', 'total_amount', 'profit', 'date')
    filter_horizontal = ('history_products', )

@admin.register(ProductHistoryCame)
class ProductHistoryCameAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'number', 'total_amount', 'price', 'date')

@admin.register(HistoryCame)
class HistoryCameAdmin(admin.ModelAdmin):
    list_display = ('id', 'responsible', 'total_number_sold_out', 'total_amount', 'date')
    filter_horizontal = ('history_products',)

@admin.register(ProductHistoryObject)
class ProductHistoryObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'number', 'total_amount', 'profit', 'date')

@admin.register(HistoryObject)
class HistoryObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'responsible', 'history_object', 'total_number_given', 'total_amount', 'total_given_amount', 'remain_amount', 'profit', 'completed', 'date')
    filter_horizontal = ('history_products', )

@admin.register(ObjectPayment)
class ObjectPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'responsible', 'history_object', 'given_amount', 'date')

@admin.register(DokonDay)
class DokonDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'responsible', 'start_date', 'end_date')
