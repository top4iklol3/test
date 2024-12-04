from django.conf import settings
from pr7.models import Product



class CartSession:
    def __init__(self, session):
        """Инициализация корзины"""
        self.session = session
        # Используем CART_SESSION_ID из настроек
        cart = session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем пустую корзину в сессии
            cart = session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        name = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in name:
            cart[str(product.id)]['product'] = product 
            
        for item in cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item 

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()

    def decrease(self, product):
        """Уменьшить количество товара на 1"""
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            if self.cart[product_id]['quantity'] <= 0:
                del self.cart[product_id]
            self.save()

    def remove(self, product):
        """Удаление товара из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Очистить корзину"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """Подсчет стоимости товаров в корзине"""
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def get_cart_info(self):
        """Получить информацию о корзине для отладки"""
        return {
            'items': dict(self.cart),
            'total_items': len(self),
            'total_price': self.get_total_price()
        }