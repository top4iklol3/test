from django.db import models
from django.contrib.auth.models import User
from pr7.models import Product
from django import forms

# Create your models here.
class PaymentStatus(models.TextChoices):
    PENDING = "На рассмотрении"
    PROCESSED = "Обработан"
    SHIPPED = "Отправлен"
    DELIVERED = "Доставлен"

class Order(models.Model):
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_email = models.EmailField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=PaymentStatus)
    paid = models.BooleanField(default=False)
    
    def get_total_cost(self):
        return sum(item.get_total() for item in self.items.all())
    
    def __str__(self):
        return f"Order {self.id} for {self.customer_user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product} for {self.order}"
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_email']
        