from django.db import models
from main_app.models import User
# from dokon_app.models import 

class ObyektJobType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class WorkAmountJobType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class WorkAmount(models.Model):
    job_type = models.CharField(max_length=255)
    visible_obyekt = models.BooleanField(default=True, blank=True, null=True)
    first_price = models.IntegerField(default=0, blank=True, null=True)
    service_price = models.IntegerField(default=0, blank=True, null=True)
    total_completed = models.IntegerField(default=0, blank=True, null=True)
    total = models.IntegerField(default=1, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.job_type

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

    def __str__(self) -> str:
        return self.name

class Given_money(models.Model):
    obyekt = models.ForeignKey(Obyekt, on_delete=models.CASCADE)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

class Instructsiya(models.Model):
    doc = models.FileField(upload_to='instructsiya/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

class Obyekt_doc(models.Model):
    role = models.CharField(default="ishchi", max_length=100)
    obyekt = models.ForeignKey(Obyekt, on_delete=models.CASCADE)
    doc = models.FileField(upload_to='obyekt_doc/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

class Allow(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)