from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from main_app.forms import LoginForm
from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import User, Worker, WorkDay
from ishchi_app.models import Work, WorkAmount, WorkDayMoney

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
        if admin:
            response = redirect('main_app:dashboard')
            response.set_cookie('user', str(user.id))
            response.set_cookie('worker', str(admin.id))
            return response
        dokon_worker = user.workers.filter(Q(name__iexact='dokon')).first()
        if dokon_worker:
            response = redirect('dokon_app:dashboard')
            response.set_cookie('user', str(user.id))
            response.set_cookie('worker', str(dokon_worker.id))
            return response
        obyekt_worker = user.workers.filter(Q(name__iexact='obyekt')).first()
        if obyekt_worker:
            response = redirect('obyekt_app:dashboard')
            response.set_cookie('user', str(user.id))
            response.set_cookie('worker', str(obyekt_worker.id))
            return response
        ishchi_worker = user.workers.filter(Q(name__iexact='ishchi')).first()
        if ishchi_worker:
            response = redirect('ishchi_app:dashboard')
            response.set_cookie('user', str(user.id))
            response.set_cookie('worker', str(ishchi_worker.id))
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
    users_with_workers_info = []

    for user_info in User.objects.filter(workers__isnull=False).values(
        'id',
        'username',
        'first_name',
        'last_name',
        'password',
        'tel_number',
        'address',
        'workers__name',
    ):
        is_working = WorkDay.objects.filter(responsible_id=user_info['id'], end_date__isnull=True).exists()
        user_info['is_working'] = is_working
        users_with_workers_info.append(user_info)
    user_id = request.COOKIES['user']
    worker_id = request.COOKIES['worker']
    worker_type = request.user.workers.values_list('name', flat=True).first()
    context = {
        'active': 'main_1',
        'worker_type': worker_type,
        'users_with_workers_info': users_with_workers_info,
        'users_type': Worker.objects.all().values('name'),
    }
    response = render(request, 'main_app/user.html', context=context)
    return response


def create_user(request):
    if has_some_error(request): return redirect('/login/')
    if request.method=='POST':
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
            if bool(request.user.workers.filter(name__iexact='admin').first()):
                user = User.objects.get(id=user_id)
                user.username = str(request.POST.get('username'))
                user.first_name = str(request.POST.get('first_name')).capitalize()
                user.last_name = str(request.POST.get('last_name')).capitalize()
                user.tel_number = str(request.POST.get('tel_number')).capitalize()
                user.address = str(request.POST.get('address')).capitalize()
                if len(str(request.POST.get('password'))):
                    user.set_password(str(request.POST.get('password')))
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

    return redirect('main_app:dashboard')


def ishchilar_holati(request):
    if has_some_error(request): return redirect('/login/')
    users_with_work_status = []

    for user_info in User.objects.filter(workers__isnull=False).values(
        'id',
        'username',
        'first_name',
        'last_name',
        'password',
        'tel_number',
        'address',
        'workers__name',
    ):
        is_working = WorkDay.objects.filter(responsible_id=user_info['id'], end_date__isnull=True).exists()
        user_info['is_working'] = is_working
        users_with_work_status.append(user_info)
    user_id = request.COOKIES['user']
    worker_id = request.COOKIES['worker']
    worker_type = request.user.workers.values_list('name', flat=True).first()
    context = {
        'active': 'main_2',
        'worker_type': worker_type,
        'users_with_work_status': users_with_work_status,
        'users_type': Worker.objects.all().values('name'),

    }
    response = render(request, 'main_app/ishchilar_holati.html', context=context)
    return response


def start_job(request):
    if has_some_error(request): return redirect('/login/')
    referer = request.META.get('HTTP_REFERER')
    if referer and not WorkDay.objects.filter(responsible=request.user, end_date__isnull=True).exists():
        WorkDay.objects.create(responsible=request.user)
        return redirect(referer)
    else:
        return redirect('/')

def end_job(request):
    if has_some_error(request): return redirect('/login/')
    referer = request.META.get('HTTP_REFERER')
    if referer and WorkDay.objects.filter(responsible=request.user, end_date__isnull=True).exists():
        WorkDay.objects.filter(responsible=request.user, end_date__isnull=True).update(end_date=timezone.now())
        return redirect(referer)
    else:
        return redirect('/')
    

# def done_work_post(request):
#     if has_some_error(request): return redirect('/login/')

#     if request.method == 'POST':
#         try:
#             # 'quantity;1': ['0'], 'quantity;2': ['0'],
#             done_works = []
#             history_came = [request.user, 0] # responsible, earn_amount
#             for key, number in request.POST.items():
#                 if key.startswith('quantity;') and number!='0':
#                     number = int(number)
#                     product_id = int(key.split(';')[1])
#                     product_details = {
#                         'job_id': product_id,
#                         'completed': number,
#                     }
#                     work_amount = WorkAmount.objects.get(id=product_id)
#                     history_came[1]+=number*work_amount.service_price
#                     done_works.append(product_details)
#             if history_came[1]==0:
#                 messages.error(request, "Xatolik ro'y berdi!")
#             else:
#                 history_came = WorkDayMoney.objects.create(
#                     responsible=history_came[0],
#                     earn_amount=history_came[1],
#                 )
#                 for product_details in done_works:
#                     product_history = Work.objects.create(
#                         job_id=product_details['job_id'],
#                         completed=product_details['completed'],
#                     )
                    
#                     history_came.work_amount.add(product_history)
#                 calculate_worker_to_obyekt(history_came.id)
#                 messages.success(request, "Bajarilgan ishlaringiz muvaffaqqiyatli qo'shildi")
#         except Exception as e:
#             print(e)
#             messages.error(request, "Xatolik ro'y berdi!")

#     return redirect("ishchi_app:dashboard")
    

# def done_work_list(request):
#     if has_some_error(request): return redirect('/login/')

#     is_working = WorkDay.objects.filter(responsible=request.user, end_date__isnull=True).exists()
#     user_id = request.COOKIES['user']
#     worker_id = request.COOKIES['worker']
#     workdaymoneys = WorkDayMoney.objects.filter(responsible=request.user).order_by('-date')
#     worker_type = request.user.workers.values_list('name', flat=True).first()
#     context = {
#         'active': 'ishchi_3',
#         'workdaymoneys': workdaymoneys,
#         'worker_type': worker_type,
#         'position': 'end' if is_working else 'start',

#     }
#     return render(request, 'ishchi/done_work_list.html', context=context)

# def done_work_detail(request):
#     if has_some_error(request): return redirect('/login/')

#     cookies = request.COOKIES
#     selected_obyekt = int(cookies.get('workdaymoney_id', 0))
#     try:
#         work_amounts = WorkDayMoney.objects.get(id=selected_obyekt, responsible=request.user).work_amount.all()
#     except:
#         work_amounts = []
#     user_id = request.COOKIES['user']
#     worker_id = request.COOKIES['worker']
#     workdaymoneys = WorkDayMoney.objects.filter(responsible=request.user).order_by('-date')
#     worker_type = request.user.workers.values_list('name', flat=True).first()
#     context = {
#         'active': 'ishchi_4',
#         'workdaymoneys': workdaymoneys,
#         'worker_type': worker_type,
#         'work_amounts': work_amounts,
#     }
#     response = render(request, 'ishchi/done_work_detail.html', context=context)
#     if selected_obyekt==0:
#         try:
#             latest_obyekt = WorkDayMoney.objects.filter(responsible=request.user).latest('date').id
#             response.set_cookie('workdaymoney_id', str(latest_obyekt))
#         except:
#             response.set_cookie('workdaymoney_id', '0')
#     return response