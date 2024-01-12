from django.contrib import admin
from .models import User, Worker

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'tel_number', 'address', 'date')
    search_fields = ['username', 'tel_number']

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date')

# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Worker, WorkerAdmin)


# from .models import Zakazlar, Kasb_turi, PraysZakaz, PraysIshchi, Maxsulot, Xodimlar, Etirozlar
# from .models import *


# @admin.register(Zakazlar)
# class NewZakaz(admin.ModelAdmin):
#     list_display = ['ism', 'obyekt_nomi', 'tel', 'ish_turi', 'status']
#     list_filter = ['ism', 'obyekt_nomi', 'tel', 'ish_turi', 'status']
#     prepopulated_fields = {'login': ('tel',)}
#     date_hierarchy = 'publish_time'
#     search_fields = ['ism', 'obyekt_nomi', 'tel', 'ish_turi', 'status']
#     ordering = ['status', 'ism', 'obyekt_nomi', 'tel']


# @admin.register(Kasb_turi)
# class NewKasb(admin.ModelAdmin):
#     list_display = ['kasb_nomi']
#     list_filter = ['kasb_nomi']
#     search_fields = ['kasb_nomi']
#     ordering = ['kasb_nomi']


# @admin.register(PraysZakaz)
# class NewPraysZakaz(admin.ModelAdmin):
#     list_display = ['ish_turi', 'ish_narxi']
#     list_filter = ['ish_turi', 'ish_narxi']
#     search_fields = ['ish_turi', 'ish_narxi']
#     ordering = ['ish_turi', 'ish_narxi']


# @admin.register(PraysIshchi)
# class NewPraysIshchi(admin.ModelAdmin):
#     list_display = ['ish_turi', 'ish_narxi']
#     list_filter = ['ish_turi', 'ish_narxi']
#     search_fields = ['ish_turi', 'ish_narxi']
#     ordering = ['ish_turi', 'ish_narxi']


# @admin.register(Maxsulot)
# class NewMaxsulot(admin.ModelAdmin):
#     list_display = ['maxsulot_nomi', 'soni', 'narxi']
#     list_filter = ['maxsulot_nomi', 'soni', 'narxi']
#     search_fields = ['maxsulot_nomi', 'soni', 'narxi']
#     ordering = ['maxsulot_nomi', 'soni', 'narxi']


# @admin.register(Xodimlar)
# class Xodim(admin.ModelAdmin):
#     list_display = ['ism', 'kasb', 'tel', 'manzil', 'yosh']
#     list_filter = ['ism', 'kasb', 'tel', 'manzil', 'yosh']
#     search_fields = ['ism', 'kasb', 'tel', 'manzil', 'yosh']
#     ordering = ['ism', 'kasb', 'tel', 'manzil', 'yosh']


# @admin.register(Etirozlar)
# class Etiroz(admin.ModelAdmin):
#     list_display = ['ism', 'titul', 'text']
#     list_filter = ['ism', 'titul', 'text']
#     search_fields = ['ism', 'titul', 'text']
#     ordering = ['ism', 'titul', 'text']

# # admin.site.register(Etirozlar)


# @admin.register(SavdoTarixi)
# class SavdoTarix(admin.ModelAdmin):
#     list_display = ['maxsulot_nomi', 'maxsulot_soni', 'maxsulot_narxi']
#     list_filter = ['maxsulot_nomi', 'maxsulot_soni', 'maxsulot_narxi']
#     search_fields = ['maxsulot_nomi', 'maxsulot_soni', 'maxsulot_narxi']
#     ordering = ['maxsulot_nomi', 'maxsulot_soni', 'maxsulot_narxi']