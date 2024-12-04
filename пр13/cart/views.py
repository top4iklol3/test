from cart.cart import CartSession
from django.shortcuts import render
from django.http import HttpRequest
from pr7.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# Create your views here.


def cart_add(request: HttpRequest, product_id):
    cart = CartSession(request.session)
    product = get_object_or_404(Product, id=product_id)
    
    # Отладочная информация
    print(f"Session ID: {request.session.session_key}")
    print(f"Adding product {product_id} ({product.name}) to cart")
    print(f"Cart before: {cart.get_cart_info()}")
    
    try:
        cart.add(product=product, quantity=1)
        print(f"Cart after: {cart.get_cart_info()}")
        print(f"Session modified: {request.session.modified}")
        return redirect('cart_detail')
    except Exception as e:
        print(f"Error adding to cart: {str(e)}")
        raise


def cart_remove(request: HttpRequest, product_id):
    cart = CartSession(request.session)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect(reverse('cart_detail'))

def cart_detail(request: HttpRequest):
    cart = CartSession(request.session)
    return render(request, 'cart_detail.html', context={
        'cart': cart
    })

def cart_clear(request: HttpRequest):
    cart = CartSession(request.session)
    cart.clear()
    return redirect('cart_detail')

def cart_item_decrease(request: HttpRequest, product_id):
    cart = CartSession(request.session)
    product = get_object_or_404(Product, id=product_id)
    cart.decrease(product=product)
    return redirect('cart_detail')