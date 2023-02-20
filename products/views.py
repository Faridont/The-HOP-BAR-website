from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from .forms import *

def main(request):
    form = ProductAddForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
    return render(request, 'landing/main.html', locals())