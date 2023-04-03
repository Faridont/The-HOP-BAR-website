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

def orders_list(request):
    orders = None
    orderRows = []
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.all()
        orderRows = orders.orderRows.all()

    context = {"order": orders, "orderRows": orderRows}
    return render(request, "landing/orders_list.html", context)

class Checkout(View):
    template_name = 'landing/checkout.html'

    def get(self, request):
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

        return render(request, self.template_name, context)

    def post(self, request):
        form = OrderForm(request.POST)
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartRows = cart.cartRows.all()


        if form.is_valid():
            order = Order(
                firstname=form.data.get("firstname"),
                lastname=form.data.get("lastname"),
                email=form.data.get("email"),
                delivery_address=form.data.get("delivery_address"),
                is_kaspi_pay=form.data.get("pay_method") == '1',
                is_cash_pay=form.data.get("pay_method") == '2',
                user=request.user,
                completed=False
            )
            order.save()

            for cartRow in cartRows:
                print(cartRow.product)
                orderProduct, created = OrderProduct.objects.get_or_create(
                    order=order,
                    product=cartRow.product,
                    quantity=cartRow.quantity,
                )
                orderProduct.save()

                cartProduct = CartProduct.objects.get(cart=cart, product=cartRow.product)
                cartProduct.delete()

            return redirect('main')



        context = {
            "cart": cart,
            "cartRows": cartRows,
            "form": form
        }

        return render(request, self.template_name, context)