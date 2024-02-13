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
from obyekt_app.models import Obyekt, WorkAmount

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO
from django.http import FileResponse
import io

from docx import Document
from docx.shared import Pt
from docx import Document
from io import BytesIO
from django.http import FileResponse
from django.utils.translation import gettext as _
from docx.shared import Inches



def check_user(request):
    try:
        work = request.user.workers.exists()
        user = request.user
        if not user or not work:
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
            cookies = request.COOKIES
            selected_obyekt1 = int(cookies.get('worker_admin_id', 0))
            selected_obyekt2 = int(cookies.get('worker_date_admin_id', 24290))

            name = str(request.POST.get('name'))
            money = int(request.POST.get('money'))
            given_money = Money.objects.create(
                responsible_id=selected_obyekt1,
                name=name,
                given_amount=money,
                month=selected_obyekt2
            )
            given_money.save()
            messages.success(request, f"{money} pull miqdori {User.objects.get(id=selected_obyekt1).first_name}  ga muaffaqiyatli qo'shildi!")
        except Exception as e:
            print(e)
            messages.error(request, 'Xatolik yuz berdi.')

    return redirect('main_app:ishchilar_holati')

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
        month_given_amount = Money.objects.filter(responsible_id=selected_obyekt1,  month=selected_obyekt2)
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
        'real_money': given_total-work_money_earn
    }
    response = render(request, 'main_app/ishchilar_holati.html', context=context)
    try:
        response.set_cookie('worker_admin_id', str(selected_obyekt1))
        response.set_cookie('worker_date_admin_id', str(selected_obyekt2))
    except Exception as e:
        print(e)
    return response

def edit_obyekt_worker_months(request, done_work_id):
    if has_some_error(request): return redirect('/login/')
    if request.method=='POST':
        try:
            work_id = int(request.POST.get('work_id'))
            total_completed = int(request.POST.get('total_completed'))
            work_obj = Work.objects.get(id=work_id)
            diff = total_completed-work_obj.completed
            diff_price_worker = diff*work_obj.job.service_price
            diff_price_object = diff*work_obj.job.first_price
            # changing Work according to diff
            work_obj.completed = total_completed
            work_obj.save()
            # changing workdayamount according to diff
            workdaymoney_obj = work_obj.workdaymoney_set.values().first()
            workdaymoney_obj = WorkDayMoney.objects.get(id=workdaymoney_obj['id'])
            workdaymoney_obj.earn_amount += diff_price_worker
            workdaymoney_obj.save()
            # changing obyekt's work amount according to diff
            work_amount_obj = WorkAmount.objects.get(id=work_obj.job.id)
            work_amount_obj.total_completed+=diff
            work_amount_obj.save()
            # changing obyekt according to diff
            obyekt_obj = work_amount_obj.obyekt_set.values().first()
            obyekt_obj = Obyekt.objects.get(id=obyekt_obj['id'])
            obyekt_obj.real_dept-=diff_price_object
            obyekt_obj.save()

            messages.success(request, "Obyekt ni real qarzdorligi, Obyekt ishining tugatilganlar soni, Qilingan ish qiymati va Qilingan ishni soni muvaffaqiyatli o'zgardi!")
        except Exception as e:
            print(e)
            messages.error(request, 'Xatolik yuz berdi.')

    return redirect('main_app:done_work_detail')


def done_work_detail(request):
    if has_some_error(request): return redirect('/login/')

    cookies = request.COOKIES
    selected_obyekt = int(cookies.get('workdaymoney_id', 0))

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
        if selected_obyekt == 0:
            work_amounts = []
            for entry in WorkDayMoney.objects.filter(responsible_id=selected_obyekt1, date__year=selected_obyekt2 // 12,
            date__month=selected_obyekt2 % 12).order_by('-date'):
                w = entry.work_amount.all()
                for i in range(len(w)):
                    w[i].date = entry.date
                work_amounts.extend(list(w))
        else: 
            a = WorkDayMoney.objects.get(id=selected_obyekt, responsible_id=selected_obyekt1)
            work_amounts = a.work_amount.all()
            for i in range(len(work_amounts)):
                work_amounts[i].date = a.date

    except:
        work_amounts = []

    try:
        workdaymoneys = WorkDayMoney.objects.filter(responsible_id=selected_obyekt1, 
            date__year=selected_obyekt2 // 12,
            date__month=selected_obyekt2 % 12).order_by('-date')
    except Exception as e:
        print(e)
        workdaymoneys = []
    
    
    worker_type = request.user.workers.values_list('name', flat=True).first()
    context = {
        'active': 'main_3',
        'workdaymoneys': workdaymoneys,
        'worker_type': worker_type,
        'work_amounts': work_amounts,
        'all_workers': Worker.objects.get(name='Ishchi').user.all(),
        'months': months,
    }

    response = render(request, 'main_app/ishchilar_ishlari.html', context=context)
    try:
        if not work_amounts and WorkDayMoney.objects.get(id=selected_obyekt):
            response.set_cookie('workdaymoney_id', str(0))
        response.set_cookie('worker_admin_id', str(selected_obyekt1))
        response.set_cookie('worker_date_admin_id', str(selected_obyekt2))
    except Exception as e:
        print(e)
    return response



def month_accurate_format(value):
    value = int(value)
    months_table = {
        1:'Yanvar',
        2:'Fevral',
        3:'Mart',
        4:'Aprel',
        5:'May',
        6:'Iyun',
        7:'Iyul',
        8:'Avgust',
        9:'Sentyabr',
        10:'Oktabr',
        11:'Noyabr',
        0:'Dekabr',

    }
    return f'{months_table[value%12]} - {value//12}'

def spacecomma(value):
    s_text = ''
    money = str(value)[::-1]
    for i in range(len(money)//3+1):
        s_text+=money[3*i:3*i+3]+' '
    return s_text.strip()[::-1] + " so'm"

def bool_to_word(value):
    if value: return "Ha"
    return "Yo'q"


def generate_worker_pdf(request):
    buffer = BytesIO()
    doc = Document()

    # Your existing code
    month = int(request.COOKIES.get('worker_date_admin_id', 24289))
    user_id = int(request.COOKIES.get('worker_admin_id', 0))
    user = User.objects.get(id=user_id)
    moneys = Money.objects.filter(responsible=user, month=month)

    doc.add_heading(f"{user.first_name} ning {month_accurate_format(month)} hisoboti.", level=1)
    doc.add_heading("Berilgan oylik hisoboti", level=2)

    # Add table for Berilgan oylik hisoboti
    table = doc.add_table(rows=1, cols=4)
    table.width = Inches(6.5)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '№'
    hdr_cells[1].text = 'Sabab'
    hdr_cells[2].text = 'Miqdor'
    hdr_cells[3].text = 'Berilgan sana'

    for cell in hdr_cells:
        cell.paragraphs[0].alignment = 1  # Center alignment

    for index, money in enumerate(moneys):
        row_cells = table.add_row().cells
        row_cells[0].text = str(index+1)
        row_cells[1].text = money.name
        row_cells[2].text = str(spacecomma(money.given_amount))
        row_cells[3].text = money.date.strftime("%d-%m-%Y")

        for cell in row_cells:
            cell.paragraphs[0].alignment = 1  # Center alignment
    for row in table.rows:
        for cell in row.cells:
            cell.vertical_alignment = 1  # 0 for top, 1 for center, 2 for bottom
    try:
        workdaymoneys_obyekt = WorkDayMoney.objects.filter(
            responsible=user,
            date__year=month // 12,
            date__month=month % 12
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
        workdaymoneys = workdaymoneys2
    except Exception as e:
        workdaymoneys = []

    doc.add_heading("Kunlik hisobotlar", level=2)

    table = doc.add_table(rows=1, cols=4)
    table.width = Inches(6.5)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '№'
    hdr_cells[1].text = 'Obyekt nomi'
    hdr_cells[2].text = 'Miqdor'
    hdr_cells[3].text = 'Sana'

    for cell in hdr_cells:
        cell.paragraphs[0].alignment = 1
        
    for index, workdaymoney in enumerate(workdaymoneys):
        row_cells = table.add_row().cells
        row_cells[0].text = str(index+1)
        row_cells[1].text = workdaymoney['obyekt_name']
        row_cells[2].text = str(spacecomma(workdaymoney['earn_amount']))
        row_cells[3].text = workdaymoney['date'].strftime("%d-%m-%Y")

        for cell in row_cells:
            cell.paragraphs[0].alignment = 1
    for row in table.rows:
        for cell in row.cells:
            cell.vertical_alignment = 1
    
    doc.add_heading("Qilingan ishlar hisoboti", level=2)

    table = doc.add_table(rows=1, cols=5)
    table.width = Inches(6.5)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '№'
    hdr_cells[1].text = 'Ish turi'
    hdr_cells[2].text = 'Xizmat haqqi'
    hdr_cells[3].text = 'Soni'
    hdr_cells[4].text = 'Sana'

    for cell in hdr_cells:
        cell.paragraphs[0].alignment = 1
    i = 0
    for index, workdaymoney in enumerate(workdaymoneys):
        for work in workdaymoney['work_amount'].all():
            i+=1
            row_cells = table.add_row().cells
            row_cells[0].text = str(i)
            row_cells[1].text = work.job.job_type
            row_cells[2].text = str(spacecomma(work.job.service_price))
            row_cells[3].text = str(work.completed)
            row_cells[4].text = workdaymoney['date'].strftime("%d-%m-%Y")

            for cell in row_cells:
                cell.paragraphs[0].alignment = 1
    for row in table.rows:
        for cell in row.cells:
            cell.vertical_alignment = 1
    
    doc.save(buffer)
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f'{user.first_name}_{month_accurate_format(month)}.docx')

# def generate_worker_pdf(request):
#     buffer = BytesIO()
#     doc = Document()

#     month = int(request.COOKIES.get('worker_date_admin_id', 24289))
#     user_id = int(request.COOKIES.get('worker_admin_id', 0))
#     user = User.objects.get(id=user_id)
#     moneys = Money.objects.filter(responsible=user, month=month)

#     doc.add_heading(f"{user.first_name} ning {month_accurate_format(month)} hisoboti.", level=1)
#     doc.add_heading("Berilgan oylik hisoboti", level=2)

#     # Add table for Berilgan oylik hisoboti
#     table = doc.add_table(rows=1, cols=5)
#     table.style = 'Table Grid'
#     hdr_cells = table.rows[0].cells
#     hdr_cells[0].text = '№'
#     hdr_cells[1].text = 'Javobgar'
#     hdr_cells[2].text = 'Sabab'
#     hdr_cells[3].text = 'Miqdor'
#     hdr_cells[4].text = 'Berilgan sana'

#     for index, money in enumerate(moneys):
#         row_cells = table.add_row().cells
#         row_cells[0].text = str(index+1)
#         row_cells[1].text = money.responsible.first_name
#         row_cells[2].text = money.name
#         row_cells[3].text = str(spacecomma(money.given_amount))
#         row_cells[4].text = money.date.strftime("%d-%m-%Y")

#     try:
#         workdaymoneys_obyekt = WorkDayMoney.objects.filter(
#             responsible=user,
#             date__year=month // 12,
#             date__month=month % 12
#         ).order_by('-date')
#         workdaymoneys2 = []
#         for detail1 in workdaymoneys_obyekt:
#             workdaymoneys = {}
#             workdaymoneys['id']=detail1.id
#             workdaymoneys['responsible']=detail1.responsible
#             workdaymoneys['earn_amount']=detail1.earn_amount
#             workdaymoneys['work_amount']=detail1.work_amount
#             workdaymoneys['date']=detail1.date
#             work_amount2 = detail1.work_amount.first().job
#             obyekt_data = list(work_amount2.obyekt_set.values().first().values())
#             workdaymoneys['obyekt_id'] = obyekt_data[0]
#             workdaymoneys['obyekt_name'] = obyekt_data[2]
#             workdaymoneys2.append(workdaymoneys)
#         workdaymoneys = workdaymoneys2
#     except Exception as e:
#         workdaymoneys = []

#     doc.add_heading("Qilingan ishlar hisoboti", level=2)

#     # Add table for Qilingan ishlar hisoboti
#     table = doc.add_table(rows=1, cols=4)
#     table.style = 'Table Grid'
#     hdr_cells = table.rows[0].cells
#     hdr_cells[0].text = '№'
#     hdr_cells[1].text = 'Javobgar'
#     hdr_cells[2].text = 'Miqdor'
#     hdr_cells[3].text = 'Sana'

#     for index, workdaymoney in enumerate(workdaymoneys):
#         row_cells = table.add_row().cells
#         row_cells[0].text = str(index+1)
#         row_cells[1].text = workdaymoney['responsible'].first_name
#         row_cells[2].text = str(spacecomma(workdaymoney['earn_amount']))
#         row_cells[3].text = workdaymoney['date'].strftime("%d-%m-%Y")

#     doc.save(buffer)
#     buffer.seek(0)

#     return FileResponse(buffer, as_attachment=True, filename=f'{user.first_name}_{month_accurate_format(month)}.docx')
#     # Your existing code
#     # month = int(request.COOKIES.get('worker_date_admin_id', 24289))
#     # user_id = int(request.COOKIES.get('worker_admin_id', 0))
#     # user = User.objects.get(id=user_id)
#     # moneys = Money.objects.filter(responsible=user, month=month)

#     # doc.add_heading(f"{user.first_name} ning {month_accurate_format(month)} hisoboti.", level=1)
#     # doc.add_heading("Berilgan oylik hisoboti", level=2)

#     # for index, money in enumerate(moneys):
#     #     doc.add_paragraph(f"Nomer: {index+1}")
#     #     doc.add_paragraph(f"Javobgar: {money.responsible.first_name}")
#     #     doc.add_paragraph(f"Sabab: {money.name}")
#     #     doc.add_paragraph(f"Miqdor: {spacecomma(money.given_amount)}")
#     #     doc.add_paragraph(f"Berilgan sana: {money.date.strftime('%d-%m-%Y')}")
#     #     doc.add_paragraph("")

#     # try:
#     #     workdaymoneys_obyekt = WorkDayMoney.objects.filter(
#     #         responsible=user,
#     #         date__year=month // 12,
#     #         date__month=month % 12
#     #     ).order_by('-date')
#     #     workdaymoneys2 = []
#     #     for detail1 in workdaymoneys_obyekt:
#     #         workdaymoneys = {}
#     #         workdaymoneys['id']=detail1.id
#     #         workdaymoneys['responsible']=detail1.responsible
#     #         workdaymoneys['earn_amount']=detail1.earn_amount
#     #         workdaymoneys['work_amount']=detail1.work_amount
#     #         workdaymoneys['date']=detail1.date
#     #         work_amount2 = detail1.work_amount.first().job
#     #         obyekt_data = list(work_amount2.obyekt_set.values().first().values())
#     #         workdaymoneys['obyekt_id'] = obyekt_data[0]
#     #         workdaymoneys['obyekt_name'] = obyekt_data[2]
#     #         workdaymoneys2.append(workdaymoneys)
#     #     workdaymoneys = workdaymoneys2
#     # except Exception as e:
#     #     workdaymoneys = []

#     # doc.add_heading("Qilingan ishlar hisoboti", level=2)

#     # for index, workdaymoney in enumerate(workdaymoneys):
#     #     doc.add_paragraph(f"Nomer: {index+1}")
#     #     doc.add_paragraph(f"Javobgar: {workdaymoney['responsible'].first_name}")
#     #     doc.add_paragraph(f"Miqdor: {spacecomma(workdaymoney['earn_amount'])}")
#     #     doc.add_paragraph(f"Sana: {workdaymoney['date'].strftime('%d-%m-%Y')}")
#     #     doc.add_paragraph("Qilingan ishlar", style='Heading 2')

#     #     for index, work_amount_item in enumerate(workdaymoney['work_amount'].all()):
#     #         doc.add_paragraph(f"Nomer: {index+1}")
#     #         doc.add_paragraph(f"Ish turi: {work_amount_item.job.job_type}")
#     #         doc.add_paragraph(f"Bo'glangan: {bool_to_word(int(work_amount_item.job.visible_obyekt))}")
#     #         doc.add_paragraph(f"Narxi: {str(spacecomma(work_amount_item.job.service_price))}")
#     #         doc.add_paragraph(f"Bajargan soni: {str(work_amount_item.completed)}")
#     #         doc.add_paragraph(f"Ish haqqi: {str(spacecomma(work_amount_item.completed*work_amount_item.job.service_price))}")
#     #         doc.add_paragraph("")

#     # doc.save(buffer)
#     # buffer.seek(0)

#     # return FileResponse(buffer, as_attachment=True, filename=f'{user.first_name}_{month_accurate_format(month)}.docx')
    