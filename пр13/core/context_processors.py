from cart.cart import CartSession 

def cart(request):
    
    return {'cart_detail' : CartSession(request.session), }