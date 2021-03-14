import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('cart', cart)
    items = []
    order = {'get_total_cart': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Item.objects.get(id=i)
            total = (product.iprice * cart[i]['quantity'])
            order['get_total_cart'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                # item = python dictionnary or JSON
                'product': {
                    'id': product.id,
                    'iname': product.iname,
                    'iprice': product.iprice,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            if product.idigital == False:
                order['shipping'] = True
        except:
            pass
    return {'items': items, 'order': order, 'cartItems': cartItems}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, status=False)
        items = order.composition_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'items': items, 'order': order, 'cartItems': cartItems}


def guestOrder(request, data):
    # data sent by unknown guest
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    # create customer based on guest info
    customer, created = Customer.objects.get_or_create(
        cemail=email,
    )
    customer.cname = name
    # data about new customer compiled in saved, return customer
    customer.save()
    # create a new order in the database (models : Order), return order
    order = Order.objects.create(
        customer=customer,
        status=False,
    )
    # create the list of items in this order (models : Composition), no need to return as nested to order
    for item in items:
        # item['product']['id'] to fetch from utils.py python dictionnary item { product { id:id }}
        product = Item.objects.get(id=item['product']['id'])
        orderItem = Composition.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'])

    return customer, order
