from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from pr7.models import Product
from django.db.models import Q
from django.contrib.auth import login,logout
from forms import RegisterForm, LoginForm
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from account.models import Profile
from forms import ProfileForm
from order.models import OrderForm
from order.models import Order

# Create your views here.


def page_view(request):
    return render(request, 'base.html')
def reg(request):
    return render(request, 'reg.html')
def auth(request):
    return render(request, 'auth.html')
def cart(request):
    return render(request, 'cart_detail.html')
def cart_add(request):
    return render(request, 'cart_detail.html')
def cart_remove(request):
    return render(request, 'cart_detail.html')






@login_required
def user_orders(request):
    orders = Order.objects.filter(customer_user=request.user).order_by('-order_date')
    return render(request, 'user_orders.html', {'orders': orders})





def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def delete_profile(request):
    user = request.user  # Получаем текущего пользователя
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        # Сначала удаляем профиль
        profile.delete()
        # Затем удаляем пользователя (это также удалит все связанные данные)
        user.delete()
        
        # Выход из системы после удаления
        logout(request)
        
        return redirect('home')  # Перенаправление на главную страницу

    return render(request, 'delete_profile.html', {'profile': profile})


# Страница с товарами 
def catalog(request):
   product = Product.objects.all()
   return render(request, 'catalog.html', context = {
    'products' : product
   })
   
#    страница с товаром 
def singlprod(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'singlprod.html', context = {
    'products' : product
    })

# Поиск товаров 
def search(request):
    if request.method == "GET":
        search_query = request.GET.get('search', '')  # используем get() с дефолтным значением
        if search_query:
            products = Product.objects.filter(
                Q(name__icontains=search_query))   # поиск по имени
            
        else:
            products = Product.objects.all()
            
        return render(request, 'catalog.html', context={
            'products': products,
            'search_query': search_query,
            'name': 'Название'
        })
    return redirect(reverse('home'))

# регистрация
def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'reg.html', context={
        'title': 'Регистрация',
        'form': form,
    })
    
    # Авторизация
    
def login_user(request: HttpRequest):
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = LoginForm()
        return render(request, 'auth.html', context={
            'title': 'Авторизация',
            'form' : form,
        })
    
@login_required(login_url='auth')
def profile(request: HttpRequest):
    user_profile = Profile.objects.select_related('user').get(user=request.user)
    username = request.user.username  # Получаем имя пользователя
    return render(request, 'profile.html', context={
        'user': user_profile,
        'username': username  # Передаем имя пользователя в шаблон
    })

def logout_view(request):
    logout(request) 
    return redirect('home')  

# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('order_success')  # Перенаправление на страницу успеха
#     else:
#         form = OrderForm()
#     return render(request, 'order/create_order.html', {'form': form})
       