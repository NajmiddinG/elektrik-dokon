from django.db import models
from main_app.models import User
from obyekt_app.models import Obyekt, WorkAmount
from datetime import date, datetime

class Work(models.Model):
    job = models.ForeignKey(WorkAmount, on_delete=models.CASCADE)
    completed = models.IntegerField(default=0, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

class WorkDay(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    obyekt = models.ForeignKey(Obyekt, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    earn_amount = models.IntegerField(default=0, blank=True, null=True)
    work_amount = models.ManyToManyField(Work)

    def has_end_date(self):
        return bool(self.end_date)

class Money(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    given_amount = models.IntegerField(default=0, blank=True, null=True)
    total_earn = models.IntegerField(default=0, blank=True, null=True)
    year = models.IntegerField(default=2023)
    month = models.IntegerField(default=datetime.now().month)
    date = models.DateTimeField(auto_now_add=True)
