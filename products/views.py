from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from .forms import *

def main(request):
    form = ProductAddForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
    products = [0, 1, 2, 3, 4, 5, 6, 7]
    return render(request, 'landing/main.html', locals())

def registration(request):
    return render(request, 'landing/registration.html', locals())

def checkout(request):
    return render(request, 'landing/checkout.html', locals())