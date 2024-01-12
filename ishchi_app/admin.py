from django.contrib import admin
from .models import Work, WorkDay, Money

class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'completed', 'date')

class WorkDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'responsible', 'obyekt', 'start_date', 'end_date', 'earn_amount')
    filter_horizontal = ('work_amount',)  # This allows a multi-select widget for work_amount

class MoneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'responsible', 'name', 'given_amount', 'total_earn', 'year', 'month', 'date')

# Register models
admin.site.register(Work, WorkAdmin)
admin.site.register(WorkDay, WorkDayAdmin)
admin.site.register(Money, MoneyAdmin)
