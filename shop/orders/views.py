from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import Order, OrderItem


def confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/confirmation.html', {'order': order})


@login_required  # Декоратор, требующий аутентификации пользователя
def checkout(request, delivery_cost=300.00):
    cart = Cart(request)
    order = None

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Создание заказа на основе данных формы
            order = form.save(commit=False)  # Создать заказ, но не сохранять его в базе данных
            if request.user.is_authenticated:
                # Если пользователь авторизован, свяжите заказ с этим пользователем
                order.user = request.user
            order.save()  # Теперь сохраните заказ в базе данных

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()

            # Измените эту часть кода, чтобы передать объект заказа на страницу confirmation
            return redirect('orders:confirmation', order_id=order.id)
    else:
        if request.user.is_authenticated:
            # Если пользователь авторизован, предзаполните форму данными пользователя
            user = request.user
            form = OrderCreateForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'email': user.email,
                'address': user.address,
                'postal_code': user.postal_code,
                'city': user.city,
            })
        else:
            form = OrderCreateForm()

    total_price = cart.get_total_price(delivery_cost=delivery_cost)
    return render(request, 'orders/order/checkout.html', {'cart': cart, 'form': form, 'delivery_cost': delivery_cost,
                                                          'total_price': total_price, 'order': order})


def auth_login2(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('orders:checkout')
        else:
            pass
    return render(request, 'orders/order/checkout.html')


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


def auth_login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:product_list')
        else:
            pass
    return render(request, 'orders/order/login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('orders:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'orders/order/register.html', {'form': form})
