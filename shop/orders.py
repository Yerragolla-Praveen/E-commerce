from django.db import models
from django.conf import settings
from .product import Product
# from .orderitem import OrderItem


class Order(models.Model):
    products = models.ManyToManyField(Product, through='OrderItem')
