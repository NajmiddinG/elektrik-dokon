from django.contrib import admin
from .models import WorkAmount, Obyekt

class WorkAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_type', 'service_price', 'total_completed', 'total', 'date')

class ObyektAdmin(admin.ModelAdmin):
    list_display = ('id', 'responsible', 'name', 'address', 'job_type', 'deal_amount', 'given_amount', 'real_dept', 'completed', 'max_dept', 'date')
    filter_horizontal = ('work_amount',)  # This allows a multi-select widget for work_amount


# Register models
admin.site.register(WorkAmount, WorkAmountAdmin)
admin.site.register(Obyekt, ObyektAdmin)
