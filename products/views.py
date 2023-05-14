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
        orders = Order.objects.all().filter(user=request.user)

    return render(request, 'landing/main.html', locals())

def product(request, id):
    cart = None
    orders = []
    product = Product.objects.get(id=id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        orders = Order.objects.all().filter(user=request.user)

    context = {
        "cart": cart,
        "orders": orders,
        "product": product
    }

    return render(request, 'landing/product.html', context)

def cart(request):
    cart = None
    cartRows = []
    orders = []

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartRows = cart.cartRows.all()
        orders = Order.objects.all().filter(user=request.user)

    context = {
        "cart": cart,
        "cartRows": cartRows,
        "orders": orders
    }

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

    return JsonResponse(num_of_item, safe=False)

def orders_list(request):
    orders = Order.objects.all().filter(user=request.user)
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

    context = {
        "orders": orders,
        "cart": cart
    }

    return render(request, "landing/orders_list.html", context)

def order(request, id):
    orders = Order.objects.all().filter(user=request.user)
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    order = Order.objects.get(id=id)
    orderRows = order.orderRows.all()

    print(order)

    context = {
        "orders": orders,
        "cart": cart,
        "order": order,
        "orderRows": orderRows
    }

    return render(request, "landing/order.html", context)

def about_us(request):
    cart = None
    orders = []

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        orders = Order.objects.all().filter(user=request.user)

    context = {
        "cart": cart,
        "orders": orders
    }

    return render(request, 'landing/about_us.html', context)
class Checkout(View):
    template_name = 'landing/checkout.html'

    def get(self, request):
        cart = None
        cartRows = []
        orders = []
        form = OrderForm()

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
            cartRows = cart.cartRows.all()
            orders = Order.objects.all().filter(user=request.user)

        context = {
            "cart": cart,
            "cartRows": cartRows,
            "form": form,
            "orders": orders
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