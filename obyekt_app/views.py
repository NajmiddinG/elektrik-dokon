from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from main_app.views import has_some_error
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import Obyekt, WorkAmount, WorkAmountJobType, ObyektJobType, Given_money, Instructsiya, Obyekt_doc
from main_app.models import Worker, User, WorkDay
from main_app.calculate import calculate_all_from_zero
import os
from django.conf import settings


def dashboard(request):
    if has_some_error(request): return redirect('/login/')

    is_working = WorkDay.objects.filter(responsible=request.user, end_date__isnull=True).exists()

    if bool(request.user.workers.filter(name__iexact='admin').first()):
        obyekts = Obyekt.objects.all().order_by('-date')
    else:
        obyekts = Obyekt.objects.filter(responsible=request.user).order_by('-date')
    obyekt_workers = User.objects.filter(workers__name='Obyekt')
    worker_type = request.user.workers.values_list('name', flat=True).first()
    obyektjobtypes = ObyektJobType.objects.all().order_by('name')
    workeramountjobtypes = WorkAmountJobType.objects.all().order_by('name')
    context = {
        'active': 'obyekt_1',
        'obyekts': obyekts,
        'obyekt_workers': obyekt_workers,
        'worker_type': worker_type,
        'obyektjobtypes': obyektjobtypes,
        'workeramountjobtypes': workeramountjobtypes,
        'position': 'end' if is_working else 'start',

    }
    return render(request, 'obyekt/obyekt.html', context=context)

def create_obyekt(request):
    if has_some_error(request): return redirect('/login/')
    if request.method=='POST':
        try:
            name = str(request.POST.get('name')).capitalize()
            obyekt_worker = request.POST.get('obyekt_worker')
            address = str(request.POST.get('address'))
            job_type = str(request.POST.get('job_type')).capitalize()
            deal_amount = request.POST.get('deal_amount')
            given_amount = request.POST.get('given_amount')
            max_dept = request.POST.get('max_dept')
            if Obyekt.objects.filter(name=name).exists():
                messages.error(request, 'Bu nomli obyekt mavjud.')
            else:
                obyekt_worker_user = User.objects.get(id=obyekt_worker)
                new_obyekt = Obyekt(
                    responsible=obyekt_worker_user,
                    name=name,
                    address=address,
                    job_type=job_type,
                    deal_amount=deal_amount,
                    given_amount=given_amount,
                    max_dept=max_dept,
                )
                new_obyekt.save()

                messages.success(request, f'{name} obyekt muvaffaqiyatli yaratildi.')
        except:
            messages.error(request, 'Xatolik yuz berdi.')

    return redirect('obyekt_app:dashboard')

def create_obyekt_job_type(request):
    if has_some_error(request): return redirect('/login/')
    if request.method=='POST':
        try:
            name = str(request.POST.get('name')).capitalize()
            if ObyektJobType.objects.filter(name=name).exists():
                messages.error(request, 'Bu nomli Obyekt ish turi mavjud.')
            else:
                new_job_type = ObyektJobType(name=name,)
                new_job_type.save()
                messages.success(request, f'{name} Obyekt ish turi muvaffaqiyatli yaratildi.')
        except:
            messages.error(request, 'Xatolik yuz berdi.')

    return redirect('obyekt_app:dashboard')

def edit_obyekt(request, obyekt_id):
    if has_some_error(request): return redirect('/login/')
    if request.method == 'POST':
        try:
            obyekt = Obyekt.objects.get(id=obyekt_id)
            obyekt.name = str(request.POST.get('name')).capitalize()
            if bool(request.user.workers.filter(name__iexact='admin').first()):
                obyekt.responsible = User.objects.get(id=request.POST.get('obyekt_worker'))
                obyekt.address = str(request.POST.get('address'))
                obyekt.job_type = str(request.POST.get('job_type')).capitalize()
                obyekt.deal_amount = request.POST.get('deal_amount')
                obyekt.given_amount = request.POST.get('given_amount')
                obyekt.max_dept = request.POST.get('max_dept')
            obyekt.save()
            messages.success(request, f'{obyekt.name} obyekt muvaffaqiyatli o\'zgartirildi.')
        except User.DoesNotExist:
            messages.error(request, 'Bunday id ga ega foydalanuvchi mavjud emas.')

    return redirect('obyekt_app:dashboard')


def obyekt_ishi(request):
    if has_some_error(request): return redirect('/login/')

    cookies = request.COOKIES
    selected_obyekt = int(cookies.get('obyekt_id', 0))
    try:
        work_amounts = Obyekt.objects.get(pk=selected_obyekt).work_amount.all()
        if bool(request.user.workers.filter(name__iexact='admin').first()):
            obyekt_doc = Obyekt_doc.objects.filter(obyekt=Obyekt.objects.get(pk=selected_obyekt)).order_by('role')
        else:
            obyekt_doc = Obyekt_doc.objects.filter(role='obyekt', obyekt=Obyekt.objects.get(pk=selected_obyekt))
    except:
        work_amounts = []
        obyekt_doc = []

    if bool(request.user.workers.filter(name__iexact='admin').first()):
        obyekts = Obyekt.objects.all().order_by('-date')
    else:
        obyekts = Obyekt.objects.filter(responsible=request.user).order_by('-date')
    obyekt_workers = User.objects.filter(workers__name='Obyekt')
    worker_type = request.user.workers.values_list('name', flat=True).first()
    obyektjobtypes = ObyektJobType.objects.all().order_by('name')
    workeramountjobtypes = WorkAmountJobType.objects.all().order_by('name')
    context = {
        'active': 'obyekt_2',
        'obyekts': obyekts,
        'obyekt_workers': obyekt_workers,
        'worker_type': worker_type,
        'work_amounts': work_amounts,
        'obyektjobtypes': obyektjobtypes,
        'workeramountjobtypes': workeramountjobtypes,
        'obyekt_doc': obyekt_doc,
    }
    response = render(request, 'obyekt/obyekt_ishi.html', context=context)
    return response


def create_obyekt_ishi(request):
    if has_some_error(request): return redirect('/login/')
    if request.method=='POST':
        try:
            obyekt = Obyekt.objects.get(id=request.POST.get('obyekt_worker'))
            work_amount = WorkAmount(
                job_type=str(request.POST.get('job_type')).capitalize(),
                visible_obyekt = bool(request.POST.get('visible_obyekt')=='on'),
                first_price=request.POST.get('first_price'),
                service_price=request.POST.get('service_price'),
                total_completed=request.POST.get('total_completed'),
                total=request.POST.get('total'),
            )
            work_amount.save()
            obyekt_id = request.POST.get('obyekt_worker')
            obyekt = get_object_or_404(Obyekt, id=obyekt_id)
            obyekt.work_amount.add(work_amount)
            messages.success(request, f'{obyekt.name} ga  muvaffaqiyatli ish yaratildi.')
            response = redirect('obyekt_app:obyekt_ishi')
            response.set_cookie('obyekt_id', str(obyekt_id))
            return response
        except:
            messages.error(request, 'Xatolik yuz berdi.')
    return redirect('obyekt_app:obyekt_ishi')

def create_work_amount_job_type(request):
    if has_some_error(request): return redirect('/login/')
    if request.method=='POST':
        try:
            name = str(request.POST.get('name')).capitalize()
            if WorkAmountJobType.objects.filter(name=name).exists():
                messages.error(request, 'Bu nomli Ish turi ish turi mavjud.')
            else:
                new_job_type = WorkAmountJobType(name=name,)
                new_job_type.save()
                messages.success(request, f'{name} Ish turi ish turi muvaffaqiyatli yaratildi.')
        except:
            messages.error(request, 'Xatolik yuz berdi.')
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('/')

def edit_obyekt_ishi(request, obyekt_id):
    if has_some_error(request): return redirect('/login/')
    if request.method == 'POST':
        try:
            # 'obyekt_worker': ['2'], 'job_type': ['2'], 'service_price': ['4'], 'total_completed': ['5'], 'total': ['9']
            if bool(request.user.workers.filter(name__iexact='admin').first()):
                work_amount = WorkAmount.objects.get(id=obyekt_id)
                work_amount.job_type = str(request.POST.get('job_type')).capitalize()
                work_amount.visible_obyekt = bool(request.POST.get('visible_obyekt')=='on')
                work_amount.first_price = request.POST.get('first_price')
                work_amount.service_price = request.POST.get('service_price')
                work_amount.total_completed = request.POST.get('total_completed')
                work_amount.total = request.POST.get('total')
                work_amount.save()

                new_obyekt_id = request.POST.get('obyekt_worker')
                new_obyekt = get_object_or_404(Obyekt, id=new_obyekt_id)

                # Remove the WorkAmount from the old Obyekt
                old_obyekt = work_amount.obyekt_set.first()  # Assuming a WorkAmount can be associated with only one Obyekt
                if old_obyekt:
                    old_obyekt.work_amount.remove(work_amount)

                # Add the WorkAmount to the new Obyekt
                new_obyekt.work_amount.add(work_amount)

                messages.success(request, f"{obyekt_id} id obyekt ma'lumotlari muvaffaqiyatli o\'zgartirildi.")
                response = redirect('obyekt_app:obyekt_ishi')
                response.set_cookie('obyekt_id', str(new_obyekt.id))
                return response
        except User.DoesNotExist:
            messages.error(request, 'Bunday id ga ega foydalanuvchi mavjud emas.')

    return redirect('obyekt_app:dashboard')

def set_obyekt_cookie(request, obyekt_id):
    referer = request.META.get('HTTP_REFERER')
    response = HttpResponseRedirect(referer or '/')
    response.set_cookie('obyekt_id', str(obyekt_id))
    
    return response


def set_obyekt_cookie2(request, obyekt_id):
    referer = request.META.get('HTTP_REFERER')
    response = HttpResponseRedirect(referer or '/')
    response.set_cookie('workdaymoney_id', str(obyekt_id))
    
    return response

def calculate_all_from_zero_view(request):
    if has_some_error(request): return redirect('/login/')

    if bool(request.user.workers.filter(name__iexact='admin').first()):
        calculate_all_from_zero()
        referer = request.META.get('HTTP_REFERER')
        response = HttpResponseRedirect(referer or '/')
        return response
    return redirect('/login/')

def create_obyekt_given_amount(request):
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

def given_money_views(request):
    if has_some_error(request): return redirect('/login/')

    cookies = request.COOKIES
    selected_obyekt = int(cookies.get('obyekt_id', 0))
    try:
        work_amounts = Given_money.objects.filter(obyekt_id=selected_obyekt)
    except:
        work_amounts = []
    if bool(request.user.workers.filter(name__iexact='admin').first()):
        obyekts = Obyekt.objects.all().order_by('-date')
    else:
        return redirect('/login/')
    obyekt_workers = User.objects.filter(workers__name='Obyekt')
    worker_type = request.user.workers.values_list('name', flat=True).first()
    obyektjobtypes = ObyektJobType.objects.all().order_by('name')
    workeramountjobtypes = WorkAmountJobType.objects.all().order_by('name')
    context = {
        'active': 'obyekt_3',
        'obyekts': obyekts,
        'obyekt_workers': obyekt_workers,
        'worker_type': worker_type,
        'work_amounts': work_amounts,
        'obyektjobtypes': obyektjobtypes,
        'workeramountjobtypes': workeramountjobtypes,
    }
    response = render(request, 'obyekt/given_money.html', context=context)
    if selected_obyekt==0:
        try:
            latest_obyekt = Obyekt.objects.latest('date').id
            response.set_cookie('obyekt_id', str(latest_obyekt))
        except:
            response.set_cookie('obyekt_id', '0')
    return response

def edit_obyekt_given_amount(request):
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



def create_obyekt_instruktsiya(request):
    if has_some_error(request):
        return redirect('/login/')
    
    if request.method == 'POST':
        try:
            # Access the uploaded file from request.FILES
            uploaded_file = request.FILES.get('doc')
            # Create a new Instruktsiya instance with the uploaded file
            new_instruktsiya = Instructsiya(doc=uploaded_file)
            new_instruktsiya.save()
            messages.success(request, f'Instruktsiya muvaffaqiyatli yaratildi.')
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('/')

def create_obyekt_xujjat(request, role=1):
    if has_some_error(request):
        return redirect('/login/')
    if request.method == 'POST':
        try:
            r = ['obyekt', 'ishchi'][role]
            cookies = request.COOKIES
            selected_obyekt = int(cookies.get('obyekt_id', 1))
            # Access the uploaded file from request.FILES
            uploaded_file = request.FILES.get('doc')
            # Create a new Instruktsiya instance with the uploaded file
            new_obyekt_doc = Obyekt_doc(role=r, obyekt=Obyekt.objects.get(pk=selected_obyekt), doc=uploaded_file)
            new_obyekt_doc.save()
            messages.success(request, f'Xujjat muvaffaqiyatli yaratildi.')
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('/')

def edit_doc(request, doc_id):
    pass

def delete_doc(request, doc_id):
    if has_some_error(request) or not request.user.workers.filter(name__iexact='admin').exists():
        return redirect('/login/')
    try:
        obyekt_doc = Obyekt_doc.objects.get(pk=doc_id)
    except Obyekt_doc.DoesNotExist:
        messages.error(request, "Xujjat mavjud emas")

    if obyekt_doc.doc:
        doc_path = os.path.join(settings.MEDIA_ROOT, str(obyekt_doc.doc))
        if os.path.exists(doc_path):
            os.remove(doc_path)

    # Delete the Obyekt_doc object
    obyekt_doc.delete()

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('/')