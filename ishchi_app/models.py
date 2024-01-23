from django.db import models
from main_app.models import User
from obyekt_app.models import WorkAmount
from datetime import date, datetime

class Work(models.Model):
    job = models.ForeignKey(WorkAmount, on_delete=models.CASCADE)
    completed = models.IntegerField(default=0, blank=True, null=True)

class WorkDayMoney(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    earn_amount = models.IntegerField(default=0, blank=True, null=True)
    work_amount = models.ManyToManyField(Work)
    admin_accepted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class Money(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    given_amount = models.IntegerField(default=0, blank=True, null=True)
    total_earn = models.IntegerField(default=0, blank=True, null=True)
    year = models.IntegerField(default=2023)
    month = models.IntegerField(default=datetime.now().month)
    date = models.DateTimeField(auto_now_add=True)
