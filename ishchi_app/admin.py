from django.contrib import admin
from .models import Work, WorkDayMoney, Money

class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'completed')

class WorkDayMoneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'responsible', 'earn_amount', 'admin_accepted', 'date')
    filter_horizontal = ('work_amount',)  # This allows a multi-select widget for work_amount

class MoneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'responsible', 'name', 'given_amount', 'total_earn', 'year', 'month', 'date')

# Register models
admin.site.register(Work, WorkAdmin)
admin.site.register(WorkDayMoney, WorkDayMoneyAdmin)
admin.site.register(Money, MoneyAdmin)
