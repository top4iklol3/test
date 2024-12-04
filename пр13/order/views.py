from django.shortcuts import render
from order.models import Order, OrderItem, OrderForm
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from cart.cart import CartSession
from django.contrib import messages

# Create your views here.
@login_required
def create_order(request: HttpRequest):
    cart = CartSession(request.session)
    
    # Проверка, пуста ли корзина
    if not cart:
        messages.error(request, "Ваша корзина пуста. Добавьте товары перед оформлением заказа.")
        return redirect('cart_detail')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer_user = request.user
            order.status = "На рассмотрении"
            order.save()
            for item_cart in cart:
                OrderItem.objects.create(order=order, product=item_cart['product'], quantity=item_cart['quantity'], price=item_cart['price']).save()
            cart.clear()
            return redirect(reverse('profile'))
    else:
        form = OrderForm()
    
    return render(request, 'create_order.html', {
        'form': form,
        'cart': cart,
    })
            
