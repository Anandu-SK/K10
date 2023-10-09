from django.db import models
from django_otp.plugins.otp_email.models import EmailDevice
from django.contrib.auth import get_user_model
from django.conf import settings

from Admin.models import *


class Userregister(models.Model):

    uname = models.CharField(max_length=50, null=True)

    uemail = models.CharField(max_length=50, null=True)

    upassword = models.CharField(max_length=50, null=True)

    uphonenumber = models.CharField(max_length=50, null=True)

    uaddress = models.CharField(max_length=50, null=True)

class Cart(models.Model):

    userid = models.ForeignKey(Userregister, null=True, on_delete=models.CASCADE)

    productid = models.ForeignKey(Productregister, null=True, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=0)

    total = models.IntegerField(default=0, null=True)
    
    status = models.IntegerField(default=0)

class Shippingaddress(models.Model):

    userid = models.ForeignKey(Userregister, on_delete=models.CASCADE)

    username = models.CharField(max_length=50, null=True)

    address = models.CharField(max_length=50, null=True)

    town = models.CharField(max_length=50, null=True)

    postcode = models.CharField(max_length=50, null=True)

    phone = models.CharField(max_length=50, null=True)

    email = models.CharField(max_length=50, null=True)

    date = models.DateField(auto_now_add=True, null=True)

class Order(models.Model):

    userid = models.ForeignKey(Userregister, on_delete=models.CASCADE)

    productid = models.ForeignKey(Productregister, on_delete=models.CASCADE)

    cartid = models.ForeignKey(Cart, on_delete=models.CASCADE)

    orderdate = models.DateField(auto_now_add=True, null=True)

    status = models.IntegerField(default = 0)

    orderquantity = models.IntegerField(null=True)

    total = models.CharField(null=True, max_length=50, default=0)

    each_product_total = models.CharField(null=True, max_length=50, default=0)

    tax = models.CharField(null=True, max_length=50, default=0)

    discount = models.CharField(null=True, max_length=50, default=0)

    total_bill = models.CharField(null=True, max_length=50, default=0)

class Wishlist(models.Model):

    userid = models.ForeignKey(Userregister, null=True, on_delete=models.CASCADE)

    productid = models.ForeignKey(Productregister, null=True, on_delete=models.CASCADE)

    status = models.IntegerField(default=0)
    

class Userfeedback(models.Model):

    uname = models.CharField(max_length=50, null=True)

    uemail = models.CharField(max_length=50, null=True)
    
    umessage = models.TextField(max_length=100, null=True)