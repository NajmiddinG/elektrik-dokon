from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from main_app.views import has_some_error
from django.contrib import messages

from .models import Product, ProductType
# Create your views here.

def dashboard(request):
    if has_some_error(request): return redirect('/login/')

    user_id = request.COOKIES['user']
    worker_id = request.COOKIES['worker']
    print(user_id, worker_id)
    context = {
        'active': '1',
    }
    return render(request, 'dokon/dokon.html', context=context)

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
    context = {
        'active': '2',
        "product_types": ProductType.objects.all().order_by('-date'),
        "products": products,
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
        print(request.POST)
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

def set_product_type_cookie(request, product_type_id):
    response = redirect('dokon_app:mahsulot')
    response.set_cookie('product_type', str(product_type_id))
    return response


def get_products(request):
    if request.method == 'POST' and request.is_ajax():
        product_type_id = request.POST.get('product_type_id')
        # Fetch products based on the selected product type
        products = Product.objects.filter(type_id=product_type_id)
        # Render the products into HTML
        products_html = render_to_string('products_table.html', {'products': products})
        return JsonResponse({'products_html': products_html})
    else:
        return JsonResponse({'error': 'Invalid request'})
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