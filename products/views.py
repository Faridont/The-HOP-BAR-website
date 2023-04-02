from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from .forms import *
import json
from django.http import JsonResponse

def main(request):
    form = ProductAddForm(request.POST or None)
    products = Product.objects.all()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

    return render(request, 'landing/main.html', locals())

def checkout(request):
    cart = None
    cartRows = []
    form = OrderForm()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartRows = cart.cartRows.all()

    context = {
        "cart": cart,
        "cartRows": cartRows,
        "form": form
    }

    return render(request, 'landing/checkout.html', context)

def cart(request):
    cart = None
    cartRows = []

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartRows = cart.cartRows.all()

    context = {"cart": cart, "cartRows": cartRows}
    return render(request, "landing/cart.html", context)


def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartProduct, created = CartProduct.objects.get_or_create(cart=cart, product=product)
        cartProduct.quantity += 1
        cartProduct.save()

        num_of_item = cart.num_of_items

        print(cartProduct)
    return JsonResponse(num_of_item, safe=False)

def delete_from_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cartProduct = CartProduct.objects.get(cart=cart, product=product)
        cartProduct.quantity -= 1
        cartProduct.delete()

        num_of_item = cart.num_of_items

        print(cartProduct)
    return JsonResponse(num_of_item, safe=False)