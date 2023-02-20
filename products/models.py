from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=256)
    image = models.ImageField()
    price = models.DecimalField(decimal_places=0, max_digits=2)