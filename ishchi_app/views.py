from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from main_app.views import has_some_error
from django.contrib import messages
from django.shortcuts import get_object_or_404

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

from obyekt_app.models import Obyekt, WorkAmount, WorkAmountJobType, ObyektJobType
from main_app.models import Worker, User, WorkDay


def dashboard(request):
    if has_some_error(request): return redirect('/login/')

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

    }
    return render(request, 'ishchi/obyekt.html', context=context)

def obyekt_ishi(request):
    if has_some_error(request): return redirect('/login/')

    cookies = request.COOKIES
    selected_obyekt = int(cookies.get('obyekt_id', 0))
    if selected_obyekt:
        work_amounts = Obyekt.objects.get(pk=selected_obyekt).work_amount.all()
    else:
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
    }
    response = render(request, 'ishchi/obyekt_ishi.html', context=context)
    if selected_obyekt==0:
        try:
            latest_obyekt = Obyekt.objects.latest('date').id
            response.set_cookie('obyekt_id', str(latest_obyekt))
        except:
            response.set_cookie('obyekt_id', '0')
    return response