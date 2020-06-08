# Create your models here.
from django.db import models
# product table 
# it inderits the Model class in models package
# after creating model we have to register the model to admin.py file -> rule of django
# product model
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    sub_category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    product_desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    # method to show product name instead of product object(1)
    def __str__(self):
        return self.product_name.capitalize()

# contact model
class Contact(models.Model):
    query_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=12, default="")
    query = models.CharField(max_length=500, default="")

    # method to show contact name instead of contact object(1)
    def __str__(self):
        return self.name.capitalize()

# orders model
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=12, default="")

    # method to show order name instead of order object(1)
    def __str__(self):
        return self.name.capitalize()

# update order for tracking status
class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    # method to show order name instead of orderUpdate object(1)
    def __str__(self):
        return self.update_desc[0:10] + "..."




