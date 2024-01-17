from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from main_app.forms import LoginForm
from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import get_object_or_404

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
        obyekt_worker = user.workers.filter(Q(name__iexact='obyekt')).first()
        print(obyekt_worker)
        if obyekt_worker or admin:
            response = redirect('obyekt_app:dashboard')
            response.set_cookie('user', str(user.id))
            response.set_cookie('worker', str(admin.id) if admin else str(obyekt_worker.id))
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
    from django.contrib.auth.hashers import check_password

    hashed_password = "pbkdf2_sha256$390000$PdBWB0qlA7ruy6cCWY5OYM$95lYUfR1L+bly7Z1jKFyvgdceuBfa5udCBAqwpZ1Kx8="
    plaintext_password = "qwe"

    # Check if the plaintext password matches the hashed password
    password_matches = check_password(plaintext_password, hashed_password)

    if password_matches:
        print("Password is correct!")
    else:
        print("Password is incorrect.")

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
            print(user)
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

def logout_user(request):
    logout(request)
    return redirect('/login/')

def dashboard(request):
    if has_some_error(request): return redirect('/login/')
    users_with_workers_info = User.objects.filter(workers__isnull=False).values(
        'id',
        'username',
        'first_name',
        'last_name',
        'password',
        'tel_number',
        'address',
        'workers__name'
    )
    user_id = request.COOKIES['user']
    worker_id = request.COOKIES['worker']
    worker_type = request.user.workers.values_list('name', flat=True).first()
    context = {
        'active': 'main_1',
        'worker_type': worker_type,
        'users_with_workers_info': users_with_workers_info
    }
    response = render(request, 'main_app/user.html', context=context)
    return response


def create_user(request):
    if has_some_error(request): return redirect('/login/')
    if request.method=='POST':
        print(request.POST)
        try:
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            tel_number = request.POST.get('tel_number')
            address = request.POST.get('address')
            password = request.POST.get('password')
            worker_type = request.POST.get('workers')

            # Create a new user instance
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                tel_number=tel_number,
                address=address,
            )

            user.set_password(password)

            # Find the existing worker
            existing_worker = Worker.objects.get(name=worker_type)
            existing_worker.user.add(user)
            user.save()
            existing_worker.save()
            messages.success(request, f'{first_name} muvaffaqiyatli yaratildi.')
            response = redirect('main_app:dashboard')
            return response
        except:
            messages.error(request, 'Xatolik yuz berdi.')
    return redirect('main_app:dashboard')

def edit_user(request, user_id):
    if has_some_error(request): return redirect('/login/')
    if request.method == 'POST':
        try:
            print(request.POST)
            # 'workers': ['Dokon']
            if bool(request.user.workers.filter(name__iexact='admin').first()):
                user = User.objects.get(id=user_id)
                user.username = str(request.POST.get('username')).capitalize()
                user.first_name = str(request.POST.get('first_name')).capitalize()
                user.last_name = str(request.POST.get('last_name')).capitalize()
                user.tel_number = str(request.POST.get('tel_number')).capitalize()
                user.address = str(request.POST.get('address')).capitalize()
                if len(str(request.POST.get('password'))):
                    user.set_password(str(request.POST.get('password')).capitalize())
                user.save()

                new_user_work = request.POST.get('workers')
                new_worker = get_object_or_404(Worker, name=new_user_work)

                old_user = user.workers.first()  # Assuming a WorkAmount can be associated with only one Obyekt
                if old_user:
                    old_user.user.remove(user)
                new_worker.user.add(user)

                messages.success(request, f"{user.first_name} ma'lumotlari muvaffaqiyatli o\'zgartirildi.")
                response = redirect('main_app:dashboard')
                return response
        except User.DoesNotExist:
            messages.error(request, 'Bunday id ga ega foydalanuvchi mavjud emas.')

    return redirect('main_aoo:dashboard')

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
