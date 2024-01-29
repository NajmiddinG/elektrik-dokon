from django.contrib import admin
from .models import WorkAmount, Obyekt, ObyektJobType, WorkAmountJobType, Given_money

class WorkAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_type', 'visible_obyekt', 'first_price', 'service_price', 'total_completed', 'total', 'date')

class ObyektAdmin(admin.ModelAdmin):
    list_display = ('id', 'responsible', 'name', 'address', 'job_type', 'deal_amount', 'given_amount', 'real_dept', 'completed', 'max_dept', 'date')
    filter_horizontal = ('work_amount',)  # This allows a multi-select widget for work_amount

class WorkAmountJobTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class ObyektJobTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Given_money)
class GivenMoneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'obyekt', 'responsible', 'amount', 'comment', 'date')
    search_fields = ('obyekt__name', 'responsible__username', 'amount', 'comment')
    list_filter = ('date',)

admin.site.register(WorkAmount, WorkAmountAdmin)
admin.site.register(Obyekt, ObyektAdmin)
admin.site.register(WorkAmountJobType, WorkAmountJobTypeAdmin)
admin.site.register(ObyektJobType, ObyektJobTypeAdmin)