from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from main_app.views import has_some_error
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import Product, ProductType, ProductHistorySoldOut, HistorySoldOut
from main_app.models import Worker, User
# Create your views here.

# def make_array()

def dashboard(request):
    if has_some_error(request): return redirect('/login/')

    user_id = request.COOKIES['user']
    worker_id = request.COOKIES['worker']
    products = Product.objects.all().order_by('-type__date')
    product_types = ProductType.objects.all().values('id', 'name')
    worker_type = request.user.workers.values_list('name', flat=True).first()
    context = {
        'active': '1',
        'products': products,
        'product_types': product_types,
        'worker_type': worker_type
    }
    return render(request, 'dokon/dokon.html', context=context)

def sell_product(request):
    if has_some_error(request): return redirect('/login/')
    try:
        total_money = 0
        sold_out_products = []
        history_sold_outs = [request.user, 0, 0, 0]
        for key, number in request.POST.items():
            if key.startswith('quantity;') and number!='0':
                number = int(number)
                product_id = int(key.split(';')[1])
                product = Product.objects.get(id=product_id)
                price = int(product.price*(100+product.profit_percentage)/100)
                if number>product.remain:
                    messages.error(request, "Xatolik ro'y berdi. Omborda yetarli mahsulot yo'q!")
                    return redirect('dokon_app:dashboard')
                
                total_money += price*number
                
                product_details = {
                    'product_id': product_id,
                    'quantity': number,
                    'total_amount': price * number,
                    'profit': (price - product.price) * number,
                }
                history_sold_outs[1]+=number
                history_sold_outs[2]+=price*number
                history_sold_outs[3]+=(price - product.price) * number
                sold_out_products.append(product_details)

                product.remain-=number
                product.save()

        # Create a HistorySoldOut object
        history_sold_out = HistorySoldOut.objects.create(
            responsible=history_sold_outs[0],
            total_number_sold_out=history_sold_outs[1],
            total_amount=history_sold_outs[2],
            profit=history_sold_outs[3],
        )

        # Create instances in ProductHistorySoldOut
        for product_details in sold_out_products:
            product_history = ProductHistorySoldOut.objects.create(
                type_id=product_details['product_id'],
                number=product_details['quantity'],
                total_amount=product_details['total_amount'],
                profit=product_details['profit'],
                date=history_sold_out.date
            )
            
            # Add the created ProductHistorySoldOut instance to history_sold_out's history_products
            history_sold_out.history_products.add(product_history)

    except Exception as e:
        messages.error(request, "Xatolik ro'y berdi!")

    return redirect('dokon_app:dashboard')

def mahsulot(request):
    if has_some_error(request): return redirect('/login/')

    cookies = request.COOKIES
    user_id = cookies.get('user', None)
    worker_id = cookies.get('worker', None)
    selected_product_type = int(cookies.get('product_type', 0))
    if selected_product_type:
        products = Product.objects.filter(type=selected_product_type).order_by('type', '-date')
    else:
        products = Product.objects.all().order_by('type', '-date')
    worker_type = request.user.workers.values_list('name', flat=True).first()
    context = {
        'active': '2',
        "product_types": ProductType.objects.all().order_by('-date'),
        "products": products,
        'worker_type': worker_type
    }
    response = render(request, 'dokon/mahsulot.html', context=context)
    if selected_product_type==0:
        response.set_cookie('product_type', '0')
    return response

def create_product_type(request):
    if has_some_error(request): return redirect('/login/')
    if request.method=='POST':
        name = str(request.POST['name']).capitalize()
        try:
            existing_product_type = ProductType.objects.get(name=name)
            messages.error(request, 'Bu nomli mahsulot turi mavjud.')
        except ProductType.DoesNotExist:
            ProductType.objects.create(name=name)
            messages.success(request, f'{name} mahsulot turi muvaffaqiyatli yaratildi.')

    return redirect('dokon_app:mahsulot')

def create_product(request):
    if has_some_error(request): return redirect('/login/')
    if request.method=='POST':
        product_type_id = request.POST.get('product_type')
        name = str(request.POST.get('name')).capitalize()
        price = request.POST.get('price')
        profit_percentage = request.POST.get('profit_percentage')
        remain = request.POST.get('remain')
        if Product.objects.filter(type__id=product_type_id, name=name).exists():
            messages.error(request, 'Bu nomli mahsulot turi mavjud.')
        else:
            product_type = ProductType.objects.get(id=product_type_id)
            new_product = Product(
                type=product_type,
                name=name,
                price=price,
                profit_percentage=profit_percentage,
                remain=remain
            )
            new_product.save()

            messages.success(request, f'{name} mahsulot muvaffaqiyatli yaratildi.')

    return redirect('dokon_app:mahsulot')

def edit_product_type(request, product_type_id):
    if has_some_error(request): return redirect('/login/')
    
    if request.method == 'POST':
        try:
            name = str(request.POST['name']).capitalize()
            product_type = ProductType.objects.get(id=product_type_id)
            product_type.name = name
            product_type.save()
            messages.success(request, f'{name} mahsulot turi muvaffaqiyatli o\'zgartirildi.')
        except ProductType.DoesNotExist:
            messages.error(request, 'Bunday id ga ega mahsulot turi mavjud emas.')
    return redirect('dokon_app:mahsulot')

def edit_product(request, product_id):
    if has_some_error(request): return redirect('/login/')
    
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            product.name = str(request.POST['name']).capitalize()
            product.type = ProductType.objects.get(id=request.POST.get('product_type'))
            product.price = request.POST.get('price')
            product.profit_percentage = request.POST.get('profit_percentage')
            if bool(request.user.workers.filter(name__iexact='admin').first()):
                product.remain = request.POST.get('remain')
            product.save()
            messages.success(request, f'{product.name} mahsulot turi muvaffaqiyatli o\'zgartirildi.')
        except ProductType.DoesNotExist:
            messages.error(request, 'Bunday id ga ega mahsulot turi mavjud emas.')
    return redirect('dokon_app:mahsulot')

def set_product_type_cookie(request, product_type_id):
    response = redirect('dokon_app:mahsulot')
    response.set_cookie('product_type', str(product_type_id))
    return response


# def get_products(request):
#     if request.method == 'POST' and request.is_ajax():
#         product_type_id = request.POST.get('product_type_id')
#         # Fetch products based on the selected product type
#         products = Product.objects.filter(type_id=product_type_id)
#         # Render the products into HTML
#         products_html = render_to_string('products_table.html', {'products': products})
#         return JsonResponse({'products_html': products_html})
#     else:
#         return JsonResponse({'error': 'Invalid request'})
# def zakaz(request):
#     if has_some_error(request): return redirect('/login/')

#     user_id = request.COOKIES['user']
#     worker_id = request.COOKIES['worker']
#     print(user_id, worker_id)
#     context = {
#         'active': '3',
#     }
#     return render(request, 'dokon/zakaz.html', context=context)

# def etiroz(request):
#     if has_some_error(request): return redirect('/login/')

#     user_id = request.COOKIES['user']
#     worker_id = request.COOKIES['worker']
#     print(user_id, worker_id)
#     context = {
#         'active': '4',
#     }
#     return render(request, 'dokon/etiroz.html', context=context)