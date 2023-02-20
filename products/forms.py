from django import forms
from .models import *


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = [""]