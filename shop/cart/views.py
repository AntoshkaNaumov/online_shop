from myshop.models import Product
from .cart import Cart
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    update_quantity = request.POST.get('update', False)

    if update_quantity:
        cart.add(product=product, quantity=quantity, update_quantity=True)
    else:
        cart.add(product=product, quantity=quantity)

    return HttpResponseRedirect(f"{reverse('shop:product_list')}?added_to_cart={product.id}")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})
