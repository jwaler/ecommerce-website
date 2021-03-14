from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder


def store(request):
    data = cartData(request)  # Call function in utils (DRY clean code)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    allproduct = Item.objects.all()
    context = {'allproduct': allproduct, 'cartItems': cartItems}
    template = 'store/store.html'
    return render(request, template, context)


def cart(request):
    data = cartData(request)  # Call function in utils (DRY clean code)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    template = 'store/cart.html'
    return render(request, template, context)


def checkout(request):
    data = cartData(request)  # Call function in utils (DRY clean code)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,
               'cartItems': cartItems}
    template = 'store/checkout.html'
    return render(request, template, context)


def payment(request):
    data = cartData(request)  # Call function in utils (DRY clean code)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,
               'cartItems': cartItems}
    template = 'store/payment.html'
    return render(request, template, context)


def login(request):
    context = {}
    return render(request, 'user/login.html', context)


def register(request):
    context = {}
    return render(request, 'user/register.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Item.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, status=False)
    composition, created = Composition.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        composition.quantity = (composition.quantity+1)

    elif action == 'remove':
        composition.quantity = (composition.quantity-1)

    composition.save()
    if composition.quantity <= 0:
        composition.delete()

    return JsonResponse("Item added", safe=False)


@csrf_exempt
def processOrder(request):
    print('data', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, status=False)

    else:
        customer, order = guestOrder(request, data)
    # Then start fill up total from form and transaction id to save the order onto the server
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_total_cart:
        order.status = True
        order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('payment complete', safe=False)
