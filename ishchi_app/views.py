from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from main_app.views import has_some_error
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Min, Max

from dokon_app.models import (
    ProductType,
    Product,
    ProductHistorySoldOut,
    HistorySoldOut,
    ProductHistoryCame,
    HistoryCame,
    ProductHistoryObject,
    HistoryObject,
    ObjectPayment,
)
from main_app.models import Worker, User, WorkDay
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from main_app.views import has_some_error
from django.contrib import messages
from django.shortcuts import get_object_or_404

from obyekt_app.models import Obyekt, WorkAmount, WorkAmountJobType, ObyektJobType, Allow, Instructsiya
from main_app.models import Worker, User, WorkDay
from ishchi_app.models import Work, WorkDayMoney, Money
from main_app.calculate import calculate_worker_to_obyekt


def dashboard(request):
    if has_some_error(request): return redirect('/login/')

    has_allow_entry = Allow.objects.filter(responsible=request.user).exists()
    instruktsiya_doc = Instructsiya.objects.all()
    is_working = WorkDay.objects.filter(responsible=request.user, end_date__isnull=True).exists()
    user_id = request.COOKIES['user']
    worker_id = request.COOKIES['worker']
    obyekts = Obyekt.objects.all().order_by('-date')
    obyekt_workers = User.objects.filter(workers__name='Obyekt')
    worker_type = request.user.workers.values_list('name', flat=True).first()
    obyektjobtypes = ObyektJobType.objects.all().order_by('name')
    workeramountjobtypes = WorkAmountJobType.objects.all().order_by('name')
    context = {
        'active': 'ishchi_1',
        'obyekts': obyekts,
        'obyekt_workers': obyekt_workers,
        'worker_type': worker_type,
        'obyektjobtypes': obyektjobtypes,
        'workeramountjobtypes': workeramountjobtypes,
        'position': 'end' if is_working else 'start',
        'allowed': has_allow_entry,
        'instruktsiya': instruktsiya_doc,

    }
    return render(request, 'ishchi/obyekt.html', context=context)

def obyekt_ishi(request):
    if has_some_error(request): return redirect('/login/')

    has_allow_entry = Allow.objects.filter(responsible=request.user).exists()
    instruktsiya_doc = Instructsiya.objects.all()
    cookies = request.COOKIES
    selected_obyekt = int(cookies.get('obyekt_id', 0))
    try:
        work_amounts = Obyekt.objects.get(pk=selected_obyekt).work_amount.all()
    except:
        work_amounts = []
    user_id = request.COOKIES['user']
    worker_id = request.COOKIES['worker']
    obyekts = Obyekt.objects.all().order_by('-date')
    obyekt_workers = User.objects.filter(workers__name='Obyekt')
    worker_type = request.user.workers.values_list('name', flat=True).first()
    obyektjobtypes = ObyektJobType.objects.all().order_by('name')
    workeramountjobtypes = WorkAmountJobType.objects.all().order_by('name')
    context = {
        'active': 'ishchi_2',
        'obyekts': obyekts,
        'obyekt_workers': obyekt_workers,
        'worker_type': worker_type,
        'work_amounts': work_amounts,
        'obyektjobtypes': obyektjobtypes,
        'workeramountjobtypes': workeramountjobtypes,
        'allowed': has_allow_entry,
        'instruktsiya': instruktsiya_doc,
    }
    response = render(request, 'ishchi/obyekt_ishi.html', context=context)
    if selected_obyekt==0:
        try:
            latest_obyekt = Obyekt.objects.latest('date').id
            response.set_cookie('obyekt_id', str(latest_obyekt))
        except:
            response.set_cookie('obyekt_id', '0')
    return response

def done_work_post(request):
    if has_some_error(request): return redirect('/login/')

    if request.method == 'POST':
        try:
            # 'quantity;1': ['0'], 'quantity;2': ['0'],
            done_works = []
            history_came = [request.user, 0] # responsible, earn_amount
            for key, number in request.POST.items():
                if key.startswith('quantity;') and number!='0':
                    number = int(number)
                    product_id = int(key.split(';')[1])
                    product_details = {
                        'job_id': product_id,
                        'completed': number,
                    }
                    work_amount = WorkAmount.objects.get(id=product_id)
                    history_came[1]+=number*work_amount.service_price
                    done_works.append(product_details)
            if history_came[1]==0:
                messages.error(request, "Xatolik ro'y berdi!")
            else:
                history_came = WorkDayMoney.objects.create(
                    responsible=history_came[0],
                    earn_amount=history_came[1],
                )
                for product_details in done_works:
                    product_history = Work.objects.create(
                        job_id=product_details['job_id'],
                        completed=product_details['completed'],
                    )
                    
                    history_came.work_amount.add(product_history)
                calculate_worker_to_obyekt(history_came.id)
                messages.success(request, "Bajarilgan ishlaringiz muvaffaqqiyatli qo'shildi")
        except Exception as e:
            print(e)
            messages.error(request, "Xatolik ro'y berdi!")

    return redirect("ishchi_app:dashboard")
    

def done_work_list(request):
    if has_some_error(request): return redirect('/login/')
    try:
        first_date = WorkDayMoney.objects.filter(responsible=request.user).aggregate(Min('date'))['date__min']
        last_date = WorkDayMoney.objects.filter(responsible=request.user).aggregate(Max('date'))['date__max']
        first_one = 12*first_date.year+first_date.month
        last_one = 12*last_date.year+last_date.month
        months = [i for i in range(first_one, last_one+1)]
    except:
        months = []
    is_working = WorkDay.objects.filter(responsible=request.user, end_date__isnull=True).exists()
    user_id = request.COOKIES['user']
    worker_id = request.COOKIES['worker']
    cookies = request.COOKIES
    selected_obyekt = int(cookies.get('worker_months', 24289))
    if selected_obyekt in [0, 24287]:
        selected_obyekt = 24289
        
    try:
        workdaymoneys_obyekt = WorkDayMoney.objects.filter(
            responsible=request.user,
            date__year=selected_obyekt // 12,
            date__month=selected_obyekt % 12
        ).order_by('-date')
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
            # print(workdaymoneys)
        workdaymoneys = workdaymoneys2
    except Exception as e:
        print(e)
        workdaymoneys = WorkDayMoney.objects.filter(responsible=request.user).order_by('-date')

    work_money_earn = 0
    for workdaymoney_item in workdaymoneys:
        work_money_earn += workdaymoney_item['earn_amount']
    
    worker_type = request.user.workers.values_list('name', flat=True).first()
    context = {
        'active': 'ishchi_3',
        'workdaymoneys': workdaymoneys,
        'worker_type': worker_type,
        'position': 'end' if is_working else 'start',
        'months': months,
        'work_money_earn': work_money_earn,

    }
    response = render(request, 'ishchi/done_work_list.html', context=context)
    response.set_cookie('worker_months', selected_obyekt)
    return response

def done_work_detail(request):
    if has_some_error(request): return redirect('/login/')

    cookies = request.COOKIES
    selected_obyekt = int(cookies.get('workdaymoney_id', 0))
    try:
        work_amounts = WorkDayMoney.objects.get(id=selected_obyekt, responsible=request.user).work_amount.all()
    except:
        work_amounts = []
    user_id = request.COOKIES['user']
    worker_id = request.COOKIES['worker']
    workdaymoneys = WorkDayMoney.objects.filter(responsible=request.user).order_by('-date')
    worker_type = request.user.workers.values_list('name', flat=True).first()
    context = {
        'active': 'ishchi_4',
        'workdaymoneys': workdaymoneys,
        'worker_type': worker_type,
        'work_amounts': work_amounts,
    }
    response = render(request, 'ishchi/done_work_detail.html', context=context)
    if selected_obyekt==0:
        try:
            latest_obyekt = WorkDayMoney.objects.filter(responsible=request.user).latest('date').id
            response.set_cookie('workdaymoney_id', str(latest_obyekt))
        except:
            response.set_cookie('workdaymoney_id', '0')
    return response


def allow_add(request):
    if has_some_error(request):
        return redirect('/login/')
    
    if request.method == 'POST':
        try:
            Allow.objects.create(responsible=request.user)
            messages.success(request, 'Juda soz.')
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('/')