from django.db import models
from .category  import Category
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=30)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    image=models.ImageField(upload_to='img')
    desc=models.TextField()
    price=models.IntegerField()

    #static method
    @staticmethod
    def get_category_id(get_id):
        if get_id:
            return Product.objects.filter(category=get_id)
        else:
            return Product.objects.all()

# class Cartitem(models.Model):
#     product=models.ForeignKey(Product,on_delete=models.CASCADE)
#     quantity=models.IntegerField(default=1)
    
#     def __str__(self):
#         return self.product.name+''+self.quantity