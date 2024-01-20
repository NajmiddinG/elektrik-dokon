from django.db import models
from main_app.models import User
from obyekt_app.models import Obyekt


class ProductType(models.Model):
    CATEGORY_CHOICES = [
        ('elektr', 'Elektga oid'),
        ('santexnika', 'Santexnikaga oid'),
    ]
    first_type = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='elektr', blank=True, null=True)
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    profit_percentage = models.IntegerField(default=0)
    remain = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class ProductHistorySoldOut(models.Model):
    type = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    profit = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)

class HistorySoldOut(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    total_number_sold_out = models.IntegerField(default=0)
    history_products = models.ManyToManyField(ProductHistorySoldOut)
    total_amount = models.IntegerField(default=0)
    profit = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)

class ProductHistoryCame(models.Model):
    type = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)

class HistoryCame(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    total_number_sold_out = models.IntegerField(default=0)
    history_products = models.ManyToManyField(ProductHistoryCame)
    total_amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)

class ProductHistoryObject(models.Model):
    type = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    profit = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

class HistoryObject(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    history_object = models.ForeignKey(Obyekt, on_delete=models.CASCADE)
    total_number_given = models.IntegerField(default=0)
    history_products = models.ManyToManyField(ProductHistoryObject)
    total_amount = models.IntegerField(default=0)
    total_given_amount = models.IntegerField(default=0)
    remain_amount = models.IntegerField(default=0)
    profit = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class ObjectPayment(models.Model):
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    history_object = models.ForeignKey(HistoryObject, on_delete=models.CASCADE)
    given_amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
