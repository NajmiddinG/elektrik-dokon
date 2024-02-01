from django.db import models
from main_app.models import User
from obyekt_app.models import WorkAmount
from datetime import date, datetime

class Work(models.Model):
    job = models.ForeignKey(WorkAmount, on_delete=models.CASCADE)
    completed = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self) -> str:
        return self.job.job_type

class WorkDayMoney(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    earn_amount = models.IntegerField(default=0, blank=True, null=True)
    work_amount = models.ManyToManyField(Work, blank=True)
    admin_accepted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.responsible.first_name

class Money(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    given_amount = models.IntegerField(default=0, blank=True, null=True)
    total_earn = models.IntegerField(default=0, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.responsible.first_name
