from cart.forms import CartAddProductForm
from .models import Category, Product, Likes, Subscription
from .form import CommentsForm
from .form import ContactForm
from .form import SubscribeForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.base import View


def search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        results = None

    return render(request, 'shop/search_results2.html', {'results': results, 'query': query})


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Проверьте, существует ли уже такая подписка (по email)
            existing_subscription = Subscription.objects.filter(email=email).first()

            if not existing_subscription:
                # Если подписки с таким email нет, создайте новую
                subscription = Subscription(email=email)
                subscription.save()
            return render(request, 'shop/thank_you.html', {'email': email})
    else:
        form = SubscribeForm()

    return render(request, 'subscribe.html', {'form': form})


def contact(request):
    return render(request, 'shop/contact.html')


def about(request):
    return render(request, 'shop/about.html')


def blog(request):
    return render(request, 'shop/blog.html')


def index(request):
    return render(request, 'shop/index.html')


def conditions(request):
    return render(request, 'shop/conditions.html')


def random_products(request):
    # Извлекаем случайные 5 товаров с одной фотографией
    products = Product.objects.filter(image_1__isnull=False).order_by('?')[:6]

    # Находим минимальный товар по цене
    min_price_product = Product.objects.filter(image_1__isnull=False).exclude(price=None).order_by('price').first()

    context = {
        'products': products,
        'min_price_product': min_price_product,
    }
    return render(request, 'shop/index.html', context)


def form_handler(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form_data = form.save()
            return render(request, 'shop/success.html', {'form_data': form_data})
    else:
        form = ContactForm()
    return render(request, 'form.html', {'form': form})


def search_product(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(request, 'shop/search_results.html', {'products': products, 'query': query})


def product_catalog1(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def product_catalog(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Добавим пагинацию
    paginator = Paginator(products, 8)  # 10 товаров на страницу
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, показываем первую страницу
        products = paginator.page(1)
    except EmptyPage:
        # Если страница вне диапазона (например, если запрос ?page=9999), показываем последнюю страницу
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def single_product(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    context = {
        'product': product
    }
    return render(request, 'shop/single-product.html', context)


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products
                  })


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})


class AddComments(View):
    """добавление комментариев"""
    def post(self, request, product_id,):
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.title = Product.objects.get(id=product_id)
            comment.save()

        product = get_object_or_404(Product, id=product_id)
        return redirect('myshop:product_detail', id=product.id, slug=product.slug)


def get_client_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


class AddLike(View):

    def get(self, request, id, slug):
        ip_client = get_client_ip(request)
        try:
            lik = Likes.objects.get(ip=ip_client, name_id=id)
            return redirect('myshop:single-product', id=id, slug=slug)
        except:
            new_like = Likes()
            new_like.name = Product.objects.get(id=id)
            new_like.ip = ip_client
            new_like.pos_id = int(id)
            new_like.save()
            return redirect('myshop:single-product', id=id, slug=slug)
