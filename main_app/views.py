from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from main_app.forms import LoginForm
from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Min, Max

from .models import User, Worker, WorkDay
from ishchi_app.models import Work, WorkAmount, WorkDayMoney, Money

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

def set_cookie_for_all_types_of_filter_view(request, name, value):
    if has_some_error(request): 
        return redirect('/login/')

    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(str(name), str(value))

    return response


def create_obyekt_worker_months(request):
    if has_some_error(request): return redirect('/login/')
    if request.method=='POST':
        try:
            obyekt_id = str(request.POST.get('obyekt_id'))
            amount = int(request.POST.get('amount'))
            comment = str(request.POST.get('comment'))
            given_money = Given_money.objects.create(
                obyekt=Obyekt.objects.get(id=obyekt_id),
                responsible=request.user,
                amount=amount,
                comment=comment,
            )
            given_money.save()
            obyekt = Obyekt.objects.get(id=obyekt_id)
            obyekt.given_amount+=amount
            obyekt.real_dept+=amount
            obyekt.save()

            messages.success(request, f"{obyekt.name} Obyektga {amount} miqdorda pull qo'shildi")
        except Exception as e:
            print(e)
            messages.error(request, 'Xatolik yuz berdi.')

    return redirect('obyekt_app:given_money_views')

def ishchilar_holati(request):
    if has_some_error(request) or not bool(request.user.workers.filter(name__iexact='admin').first()): return redirect('/login/')

    cookies = request.COOKIES
    selected_obyekt1 = int(cookies.get('worker_admin_id', 0))
    if selected_obyekt1==0:
        for user in User.objects.all():
            if user.workers.filter(name__iexact='ishchi').first():
                selected_obyekt1 = user.id
                break
    selected_obyekt2 = int(cookies.get('worker_date_admin_id', 24289))
    try:
        first_date = WorkDayMoney.objects.filter(responsible_id=selected_obyekt1).aggregate(Min('date'))['date__min']
        last_date = WorkDayMoney.objects.filter(responsible_id=selected_obyekt1).aggregate(Max('date'))['date__max']
        first_one = 12*first_date.year+first_date.month
        last_one = 12*last_date.year+last_date.month
        months = [i for i in range(first_one, last_one+1)]
    except:
        months = []
    try:
        workdaymoneys_obyekt = WorkDayMoney.objects.filter(
            responsible_id=selected_obyekt1,
            date__year=selected_obyekt2 // 12,
            date__month=selected_obyekt2 % 12
        ).order_by('-date')
        month_given_amount = Money.objects.filter(responsible_id=selected_obyekt1,  date__year=selected_obyekt2 // 12,
            date__month=selected_obyekt2 % 12)
        workdaymoneys2 = []
        for detail1 in workdaymoneys_obyekt:
            workdaymoneys = {}
            workdaymoneys['id']=detail1.id
            workdaymoneys['responsible']=detail1.responsible
            workdaymoneys['earn_amount']=detail1.earn_amount
            workdaymoneys['work_amount']=detail1.work_amount
            workdaymoneys['date']=detail1.date
            work_amount2 = detail1.work_amount.first().job
            obyekt_data = list(work_amount2.obyekt_set.values().first().values())
            workdaymoneys['obyekt_id'] = obyekt_data[0]
            workdaymoneys['obyekt_name'] = obyekt_data[2]
            workdaymoneys2.append(workdaymoneys)
        workdaymoneys = workdaymoneys2
    except Exception as e:
        print(e)
        workdaymoneys = WorkDayMoney.objects.filter(responsible_id=selected_obyekt1).order_by('-date')
        month_given_amount = Money.objects.filter(responsible_id=selected_obyekt1)
    
    work_money_earn = 0
    for workdaymoney_item in workdaymoneys:
        work_money_earn += workdaymoney_item['earn_amount']
    
    given_total = 0
    for item in month_given_amount:
        given_total+=item.given_amount
    
    obyekt_workers = User.objects.filter(workers__name='Obyekt')
    worker_type = request.user.workers.values_list('name', flat=True).first()
    print(months)
    context = {
        'active': 'main_2',
        'month_given_amount': month_given_amount,
        'obyekt_workers': obyekt_workers,
        'worker_type': worker_type,
        'work_money_earn': work_money_earn,
        'workdaymoneys': workdaymoneys,
        'given_total': given_total,
        'all_workers': Worker.objects.get(name='Ishchi').user.all(),
        'months': months,
    }
    response = render(request, 'main_app/ishchilar_holati.html', context=context)
    try:
        response.set_cookie('worker_admin_id', str(selected_obyekt1))
        response.set_cookie('worker_date_admin_id', str(selected_obyekt2))
    except Exception as e:
        print(e)
    return response

def edit_obyekt_worker_months(request):
    if has_some_error(request): return redirect('/login/')
    if request.method=='POST':
        try:
            given_money_id = str(request.POST.get('given_money_id'))
            amount = int(request.POST.get('amount'))
            comment = str(request.POST.get('comment'))
            given_money = Given_money.objects.get(id=given_money_id)
            obyekt = Obyekt.objects.get(id=given_money.obyekt.id)
            obyekt.given_amount = obyekt.given_amount-given_money.amount+amount
            obyekt.real_dept = obyekt.real_dept-given_money.amount+amount
            obyekt.save()
            given_money.amount = amount
            given_money.responsible=request.user
            given_money.amount=amount
            given_money.comment=comment
            given_money.save()

            messages.success(request, f"{given_money.id}- olingan pull {amount} ga o'zgartirildi!")
        except Exception as e:
            print(e)
            messages.error(request, 'Xatolik yuz berdi.')

    return redirect('obyekt_app:given_money_views')


# class Money(models.Model):
    # responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)
    # given_amount = models.IntegerField(default=0, blank=True, null=True)
    # total_earn = models.IntegerField(default=0, blank=True, null=True)
    # year = models.IntegerField(default=2023)
    # month = models.IntegerField(default=datetime.now().month)
    # date = models.DateTimeField(auto_now_add=True)

    # def __str__(self) -> str:
    #     return self.responsible.first_name