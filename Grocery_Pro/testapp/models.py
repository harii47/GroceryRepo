from django.db import models


class User_Model(models.Model):
    name = models.CharField(max_length=40)
    mobile = models.BigIntegerField()
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=18)
    address = models.CharField(max_length=200)


class Grocery_Item_Model(models.Model):
    item_name = models.CharField(max_length=200)
    item_status = models.CharField(max_length=200)
    item_quantity = models.CharField(max_length=200)
    date = models.DateField()


class Bought_Item(models.Model):
    grocery_item = models.ForeignKey(Grocery_Item_Model, on_delete=models.CASCADE)
    user = models.ForeignKey(User_Model, on_delete=models.CASCADE, default=1)
    quantity = models.CharField(max_length=20,default='20kg')
    item_status = models.CharField(max_length=40)
