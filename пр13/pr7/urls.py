from django.urls import path, include
from .views import page_view, catalog, singlprod, search, register, login_user, profile, logout_view, delete_profile, edit_profile
from cart.views import cart_add, cart_remove, cart_detail, cart_clear, cart_item_decrease
from order.views import create_order
from .views import user_orders 

urlpatterns = [
    path('', page_view, name='home'),
    path('catalog', catalog, name="catalog"),
    path('product/<int:pk>', singlprod, name='singlprod'),
    path('search/', search, name="search"),
    path('reg', register, name='reg'),
    path('auth', login_user, name='auth' ),
    path('profile', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/delete/', delete_profile, name='delete_profile'),
    path('cart/', cart_detail, name='cart_detail'),  # Измените этот URL
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('cart/decrease/<int:product_id>/', cart_item_decrease, name='cart_item_decrease'),
    path('create_order/', create_order, name='create_order'),
    path('my-orders/', user_orders, name='user_orders'),

]
