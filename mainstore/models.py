from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    cname = models.CharField(max_length=200, null=False, blank=False)
    cemail = models.EmailField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.cname


class Item(models.Model):
    iname = models.CharField(max_length=200, null=False, blank=False)
    iprice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    idigital = models.BooleanField(default=False, null=True, blank=False)
    idesc = models.TextField(max_length=500, null=True, blank=True)
    iimg = models.ImageField(null=True, blank=True,
                             upload_to="images/", verbose_name="Image")

    def __str__(self):
        return self.iname

    @property
    def imageURL(self):
        try:
            url = self.iimg.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.composition_set.all()
        for i in orderitems:
            if i.product.idigital == False:
                shipping = True
        return shipping

    @property
    def get_total_cart(self):
        orderitems = self.composition_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.composition_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class Composition(models.Model):
    product = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.iprice * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
