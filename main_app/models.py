from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    tel_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username

    def has_workers(self):
        return self.workers.exists()

class Worker(models.Model):
    user = models.ManyToManyField(User, related_name='workers')
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name

    





# from django.db import models
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.utils import timezone





# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status__in=[Zakazlar.Status.primary, Zakazlar.Status.danger])

# class Etirozlar(models.Model):
#     ism = models.CharField(max_length=250)
#     titul = models.CharField(max_length=250)
#     text = models.TextField()
#     publish_time = models.DateTimeField(auto_now=True)

#     objects = models.Manager()
#     published = PublishedManager()

#     def __str__(self):
#         return self.ism

# class Kasb_turi(models.Model):
#     kasb_nomi = models.CharField(max_length=150, unique=True)

#     objects = models.Manager()
#     published = PublishedManager()

#     def __str__(self):
#         return self.kasb_nomi

# class Maxsulot(models.Model):
#     maxsulot_nomi = models.CharField(max_length=250, unique=True)
#     maxsulot_default = '-----'
#     soni = models.IntegerField(null=True, blank=True)
#     narxi = models.IntegerField(null=True, blank=True)
#     foiz = models.IntegerField(null=True, blank=True)
#     foiz_narxi = models.IntegerField(null=True, blank=True)


#     objects = models.Manager()
#     published = PublishedManager()

#     def __str__(self):
#         return self.maxsulot_nomi

# class SavdoTarixi(models.Model):
#     maxsulot_nomi = models.CharField(max_length=250, default='')
#     maxsulot_soni = models.IntegerField(null=True, blank=True)
#     maxsulot_narxi = models.IntegerField(null=True, blank=True)
#     save_date = models.DateTimeField(auto_now_add=True)

#     objects = models.Manager()
#     published = PublishedManager()

#     def __str__(self):
#         return self.maxsulot_nomi

# class Xodimlar(models.Model):
#     ism = models.CharField(max_length=150)
#     tel = models.CharField(max_length=150,
#                            default='')
#     kasb = models.ForeignKey(Kasb_turi,
#                                     max_length=150,
#                                     on_delete=models.CASCADE,
#                                     to_field='kasb_nomi')
#     manzil = models.CharField(max_length=250)
#     yosh = models.DateField(default='')
#     oylik = models.IntegerField(null=True, blank=True)
#     mutaxasislig = models.CharField(max_length=250,
#                                     default='')


#     objects = models.Manager()
#     published = PublishedManager()

#     def __str__(self):
#         return self.ism

# class PraysIshchi(models.Model):
#     ish_turi = models.CharField(max_length=250, unique=True)
#     ish_narxi = models.IntegerField(null=True, blank=True)


#     objects = models.Manager()
#     published = PublishedManager()

#     def __str__(self):
#         return self.ish_turi


# class PraysZakaz(models.Model):
#     ish_turi = models.CharField(max_length=250, unique=True)
#     ish_narxi = models.IntegerField(null=True, blank=True)


#     objects = models.Manager()
#     published = PublishedManager()

#     def __str__(self):
#         return self.ish_turi


# class Zakazlar:
#     pass


# class Zakazlar(models.Model):
#     class Status(models.TextChoices):
#         danger = "dg", "danger"
#         primary = "pr", "primary"
#         history = "hs", "history"

#     ism = models.CharField(max_length=250)
#     obyekt_nomi = models.CharField(max_length=250)
#     obyekt_manzil = models.CharField(max_length=250, default='')
#     obyekt_fayli = models.FileField(upload_to='file')
#     publish_time = models.DateTimeField(default=timezone.now)
#     tel = models.CharField(max_length=250, default='')
#     ish_turi = models.ForeignKey(Kasb_turi,
#                                  on_delete=models.CASCADE)
#     kelishilgan_summa = models.IntegerField(null=True, blank=True)
#     olingan_summa = models.IntegerField(null=True, blank=True)
#     bajarilgan_summa = models.IntegerField(null=True, blank=True)
#     qoldiq = models.IntegerField(null=True, blank=True)
#     ustavka = models.IntegerField(null=True, blank=True)
#     login = models.CharField(max_length=250, default='')
#     maxsulotlar = models.ForeignKey(Maxsulot,
#                                     max_length=150,
#                                     on_delete=models.CASCADE,
#                                     to_field='maxsulot_nomi',
#                                     default=Maxsulot.maxsulot_default)
#     prays_ishchi = models.ForeignKey(PraysIshchi,
#                                      on_delete=models.CASCADE,
#                                      to_field='ish_turi')
#     prays_zakaz = models.ForeignKey(PraysZakaz,
#                                     on_delete=models.CASCADE,
#                                     to_field='ish_turi')
#     tavsif = models.TextField()
#     status = models.CharField(max_length=2,
#                               choices=Status.choices,
#                               default=Status.primary)

#     objects = models.Manager()
#     published = PublishedManager()

#     @receiver(pre_save, sender=Zakazlar)
#     def update_status(sender, instance, **kwargs):
#         # Вычисляем qoldiq
#         qoldiq = instance.olingan_summa - instance.bajarilgan_summa

#         # Проверяем условия для установки статуса
#         if (
#                 qoldiq <= -instance.ustavka
#                 or instance.kelishilgan_summa == instance.olingan_summa
#                 or instance.status == Zakazlar.Status.danger
#         ):
#             instance.status = Zakazlar.Status.danger
#         elif instance.status == Zakazlar.Status.history:
#             # Обработка логики для отображения истории
#             pass
#         else:
#             instance.status = Zakazlar.Status.primary

#     class Meta:
#         ordering = ['-publish_time']

#     def __str__(self):
#         return self.ism