from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput, EmailInput, RadioSelect

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to="media")
    price = models.DecimalField(decimal_places=0, max_digits=6)
    class Meta:
        db_table = "gallery"
    def __str__(self):
        return f'{self.name}-{self.id}'

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        cartRows = self.cartRows.all()
        total = sum([item.price for item in cartRows])
        return total

    @property
    def num_of_items(self):
        cartRows = self.cartRows.all()
        quantity = sum([item.quantity for item in cartRows])
        return quantity

class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartRows")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

    @property
    def price(self):
        new_price = self.product.price * self.quantity
        return new_price

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField(default=datetime.now(), blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    delivery_address = models.CharField(max_length=256)
    is_kaspi_pay = models.BooleanField()
    is_cash_pay = models.BooleanField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        orderRows = self.orderRows.all()
        total = sum([item.price for item in orderRows])
        return total

    @property
    def order_number(self):
        return str(self.id).zfill(5)

    @property
    def num_of_items(self):
        orderRows = self.orderRows.all()
        quantity = sum([item.quantity for item in orderRows])
        return quantity

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderRows")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.order.id}-{self.product.name}'

    @property
    def price(self):
        new_price = self.product.price * self.quantity
        return new_price

class OrderForm(forms.Form):
    CHOICES = [
        ('1', 'Kaspi Gold'),
        ('2', 'Наличные'),
    ]
    firstname = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), max_length=100)
    lastname = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), max_length=100)
    email = forms.EmailField(widget=EmailInput(attrs={'class': 'form-control'}))
    delivery_address = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), max_length=256)
    pay_method = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'hop-text-contrast-color'}), choices=CHOICES)
