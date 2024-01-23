from django.db import models
from main_app.models import User
# from dokon_app.models import 

class ObyektJobType(models.Model):
    name = models.CharField(max_length=255)


class WorkAmountJobType(models.Model):
    name = models.CharField(max_length=255)

class WorkAmount(models.Model):
    job_type = models.CharField(max_length=255)
    first_price = models.IntegerField(default=0, blank=True, null=True)
    service_price = models.IntegerField(default=0, blank=True, null=True)
    total_completed = models.IntegerField(default=0, blank=True, null=True)
    total = models.IntegerField(default=1, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

class Obyekt(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.CharField(max_length=255, blank=True, null=True)
    deal_amount = models.IntegerField(default=0, blank=True, null=True)
    given_amount = models.IntegerField(default=0, blank=True, null=True)
    work_amount = models.ManyToManyField(WorkAmount, blank=True)
    real_dept = models.IntegerField(default=0, blank=True, null=True)
    max_dept = models.IntegerField(default=100000000, blank=True, null=True)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    contract = models.FileField(upload_to='contracts/', blank=True, null=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
