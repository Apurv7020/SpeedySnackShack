from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Product(models.Model):
    CAT = ((1,"Pizza"),(2,"Burger"),(3,"Drinks"),(4,"Sandwitches & Fries"))
    name = models.CharField(max_length=50)              #Product name
    price = models.IntegerField()                       #Product Price
    cat = models.IntegerField(choices=CAT)              #Product Category
    P_details = models.CharField(max_length=150)         #Product Details
    is_active = models.BooleanField(default=True)       #To check if prduct is available
    pimage = models.ImageField(upload_to="image")       #Product Image

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_column='user_id')
    pid = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='pid')
    Qty = models.IntegerField(default=1)

class Person(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_column='user_id')
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=100)

class Feedback(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=30)
    feedback = models.CharField(max_length=200)
    submitted_at = models.DateTimeField(auto_now_add=True)  # Automatically set the date and time when the feedback is submitted

class Store(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

class Order(models.Model):
    order_id = models.CharField(max_length=50)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_column='user_id')
    pid = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='pid')
    qty = models.IntegerField(default=1)
    amount = models.IntegerField()