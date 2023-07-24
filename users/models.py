from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, null=False)
    date_placed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.id, self.user_id

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return self.order_id, self.product_id, self.id, self.quantity

