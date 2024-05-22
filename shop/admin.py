from django.contrib import admin
from .product import Product
from .category import Category
from .customer import Customer
from .orders import Order
from .orderitem import OrderItem

# Register your models here.
class categoryinfo(admin.ModelAdmin):
    list_display=["name"]

class productinfo(admin.ModelAdmin):
    list_display=["name","category","price"]


admin.site.register(Product,productinfo)
admin.site.register(Category,categoryinfo)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)

