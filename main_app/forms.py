from django import forms

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# from .models import Etirozlar, Maxsulot
# from .models import *


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Etirozlar
#         fields = "__all__"


# class MaxsulotForm(forms.ModelForm):
#     class Meta:
#         model = Maxsulot
#         fields = "__all__"

# class SavdoTarixiForm(forms.ModelForm):
#     class Meta:
#         model = SavdoTarixi
#         fields = ['maxsulot_nomi', 'maxsulot_soni', 'maxsulot_narxi']


# class XodimlarForm(forms.ModelForm):
#     class Meta:
#         model = Xodimlar
#         fields = "__all__"


# class ZakazlarForm(forms.ModelForm):
#     class Meta:
#         model = Zakazlar
#         fields = "__all__"


# class KasbForm(forms.ModelForm):
#     class Meta:
#         model = Kasb_turi
#         fields = "__all__"


# class PraysZakazForm(forms.ModelForm):
#     class Meta:
#         model = PraysZakaz
#         fields = "__all__"


# class PraysIshchiForm(forms.ModelForm):
#     class Meta:
#         model = PraysIshchi
#         fields = "__all__"


# class CombinedForm(forms.Form):
#     ish_turi = forms.CharField(max_length=250)
#     ish_narxi = forms.CharField(max_length=250)
#     tanlang = forms.ChoiceField(choices=[('Zakazchi', 'Zakazchi'), ('Ishchi', 'Ishchi')])

#     def save(self):
#         ish_turi = self.cleaned_data['ish_turi']
#         ish_narxi = self.cleaned_data['ish_narxi']
#         tanlang = self.cleaned_data['tanlang']

#         if tanlang == 'Zakazchi':
#             PraysZakaz.objects.create(ish_turi=ish_turi, ish_narxi=ish_narxi)
#         elif tanlang == 'Ishchi':
#             PraysIshchi.objects.create(ish_turi=ish_turi, ish_narxi=ish_narxi)