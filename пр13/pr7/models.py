from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    

  

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    category = models.ManyToManyField(Category, verbose_name='Категория товара')
    image = models.ImageField(upload_to="pr7/%Y/%m/%d", verbose_name='URL изображения товара')

   