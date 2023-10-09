from django.db import models


class  Productcategory(models.Model):

    cName = models.CharField(max_length=50, null=True)

    cImage = models.ImageField(upload_to='media', default='null.jpg')


class Productregister(models.Model):

    pName = models.CharField(max_length=50, null=True)

    pImage = models.ImageField(upload_to='media', default='null.jpg')

    pPrice = models.CharField(max_length=50, null=True)

    pCategory = models.ForeignKey(Productcategory , on_delete=models.CASCADE, null=True)

    pQuantity = models.IntegerField(null=True)

    pStatus = models.IntegerField(default=0)

   



