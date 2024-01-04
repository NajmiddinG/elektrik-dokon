from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from main_app.forms import LoginForm
from django.db.models import Q
from django.shortcuts import redirect, render

from .models import User, Worker

def check_user(request):
    try:
        user_id = request.COOKIES['user']
        worker_id = request.COOKIES['worker']
        
        if not user_id or not worker_id:
            return False
        user = User.objects.get(id=user_id)
        work = user.workers.filter(id=worker_id).first()
        if not work:
            return False
        return True

    except Exception as e:
        print(2, e)
        return False

def check_user_type(request):
    user = request.user
    try:
        admin = user.workers.filter(name__iexact='admin').first()
        dokon_worker = user.workers.filter(Q(name__iexact='dokon')).first()
        if dokon_worker or admin:
            response = redirect('dokon_app:dashboard')
            response.set_cookie('user', str(user.id))
            response.set_cookie('worker', str(admin.id) if admin else str(dokon_worker.id))
            return response
        logout(request)
        return redirect(user_login)
    except Exception as e:
        print(1, e)
        return HttpResponse('Tizimda xatolik')

def has_some_error(request):
    try:
        if request.user.workers.filter(name__iexact='admin').first(): return False
    except: pass
    return bool(not request.user.is_authenticated or not check_user(request))

def user_login(request):
    if request.user.is_authenticated:
        return check_user_type(request)
    
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username = data['login'],
                                password = data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return check_user_type(request)
                else:
                    return HttpResponse('Kirmadingiz')
            else:
                print(data)
                return HttpResponse('Login yoki parolda xatolik bor')
    else:
        form = LoginForm()
        context = {
            'form': form,
        }
    return render(request, 'registration/login.html', context)

def dashboard(request):
    if has_some_error(request): return redirect('/login/')
    
    return HttpResponse('Bu main app dashboard page')

# from datetime import datetime

# from django.http import HttpResponse
# from django.shortcuts import render, get_object_or_404
# # from .models import Zakazlar, Kasb_turi, PraysZakaz, PraysIshchi, Maxsulot, Xodimlar, Etirozlar
# # from .forms import ContactForm, MaxsulotForm
# from .models import *
# from .forms import *


# def admin_list(request):
#     zakaz_list = Zakazlar.objects.all()
#     ishchilar_list = Xodimlar.objects.all()
#     maxsulot_list = Maxsulot.objects.all()
#     prayszakaz_list = PraysZakaz.objects.all()
#     praysishchi_list = PraysIshchi.objects.all()
#     kasb_list = Kasb_turi.objects.all()
#     etirozlar_list = Etirozlar.objects.all()

#     formMaxsulot = MaxsulotForm(request.POST or None)
#     formXodimlar = XodimlarForm(request.POST or None)
#     formZakaz = ZakazlarForm(request.POST or None)
#     formKasb = KasbForm(request.POST or None)
#     formCombinate = CombinedForm(request.POST or None)

#     if request.method == "POST" and formMaxsulot.is_valid():
#         formMaxsulot.save()
#         # return HttpResponse("Yangi maxsulot saqlandi")
#     if request.method == "POST" and formXodimlar.is_valid():
#         formXodimlar.save()
#     if request.method == "POST" and formZakaz.is_valid():
#         formZakaz.save()
#     if request.method == "POST" and formKasb.is_valid():
#         formKasb.save()
#     if request.method == "POST" and formCombinate.is_valid():
#         formCombinate.save()
#     else:
#         print(formMaxsulot.errors, formXodimlar.errors, formKasb, formZakaz, formCombinate)
#     context = {
#         "zakaz_list": zakaz_list,
#         "ishchilar_list": ishchilar_list,
#         "maxsulot_list": maxsulot_list,
#         "prayszakaz_list": prayszakaz_list,
#         "praysishchi_list": praysishchi_list,
#         "kasb_list": kasb_list,
#         "etirozlar_list": etirozlar_list,
#         "formMaxsulot": formMaxsulot,
#         "formZakaz": formZakaz,
#         "formKasb": formKasb,
#         "formCombinate": formCombinate,
#     }

#     return render(request, 'pages/admin.html', context)


# def ishchilar_page(request):
#     zakaz_list = Zakazlar.objects.filter(status__in=[Zakazlar.Status.primary, Zakazlar.Status.danger])
#     ishchilar_list = Xodimlar.objects.all()
#     formContact = ContactForm(request.POST or None)
#     if request.method == "POST" and formContact.is_valid():
#         formContact.save()
#         return HttpResponse("Thank you!!")
#     else:
#         print(formContact.errors)

#     context = {
#         "zakaz_list": zakaz_list,
#         "ishchilar_list": ishchilar_list,
#         "formContact": formContact,
#     }

#     return render(request, 'pages/elektrik.html', context)


# def magazin_page(request):
#     zakaz_list = Zakazlar.objects.filter(status__in=[Zakazlar.Status.primary, Zakazlar.Status.danger])
#     maxsulot_list = Maxsulot.objects.all()
#     formContact = ContactForm(request.POST or None)
#     formMaxsulot = MaxsulotForm(request.POST or None)
#     formSavdoTarixi = SavdoTarixiForm(request.POST or None)

#     if request.method == "POST":
#         if formMaxsulot.is_valid():
#             maxsulot_instance = formMaxsulot.save(commit=False)

#             # Получить значение soni из формы и сохранить его в SavdoTarixi
#             soni_value = request.POST.get('soni')
#             savdo_tarixi_instance = SavdoTarixi(
#                 maxsulot_nomi=maxsulot_instance.maxsulot_nomi,
#                 maxsulot_soni=soni_value,
#                 maxsulot_narxi=maxsulot_instance.foiz_narxi
#             )
#             savdo_tarixi_instance.save()

#             # Вычесть значение soni из Maxsulot
#             maxsulot_instance.soni -= int(soni_value)
#             maxsulot_instance.save()

#             # Очистить форму после сохранения, если нужно
#             formMaxsulot = MaxsulotForm()
#             # return HttpResponse("Yangi maxsulot saqlandi")

#     if request.method == "POST" and formSavdoTarixi.is_valid():
#         formSavdoTarixi.save()

#     if request.method == "POST" and formContact.is_valid():
#         formContact.save()
#         # return HttpResponse("Thank you!!")
#     else:
#         print(formMaxsulot.errors, formContact.errors)
#     context = {
#         "zakaz_list": zakaz_list,
#         "maxsulot_list": maxsulot_list,
#         "formContact": formContact,
#         "formMaxsulot": formMaxsulot,
#         "formSavdoTarixi": formSavdoTarixi,
#     }

#     return render(request, 'pages/do`kon.html', context)

# def zakazchi_page(request):
#     zakaz_list = Zakazlar.objects.filter(status__in=[Zakazlar.Status.primary, Zakazlar.Status.danger])
#     formContact = ContactForm(request.POST or None)
#     if request.method == "POST" and formContact.is_valid():
#         formContact.save()
#         return HttpResponse("Thank you!!")
#     context = {
#         "zakaz_list": zakaz_list,
#         "formContact": formContact,
#     }

#     return render(request, 'pages/zakazchi.html', context)


# def login_page(request):
#     return render(request, 'pages/login.html')
