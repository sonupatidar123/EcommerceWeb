
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from Category.models import Category

from carts.models import CartItem
from django.db.models import Q

from carts.views import _cart_id
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct


def store(request, category_slug=None):
    categories = None
    products = None
    # Base queryset depending on category
    if category_slug:   # if slug is given
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True).order_by('id')
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

    # Price range filtering via GET params (min_price and max_price)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    try:
        if min_price:
            # allow values like "2000" (we render "₹2000+" in the UI)
            min_val = int(str(min_price).replace('+', '').strip())
            products = products.filter(price__gte=min_val)
        if max_price:
            max_val = int(str(max_price).replace('+', '').strip())
            products = products.filter(price__lte=max_val)
    except ValueError:
        # ignore malformed inputs and continue with unfiltered queryset
        pass

    # Pagination
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = []
    product_count = 0
    keyword = ''
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword'].strip()
        if keyword:
            # Search in product name and description
            products = Product.objects.filter(
                Q(product_name__icontains=keyword) | 
                Q(description__icontains=keyword)
            ).filter(is_available=True).order_by('-created_date')
            product_count = products.count()
            
            # Pagination
            paginator = Paginator(products, 12)
            page = request.GET.get('page')
            products = paginator.get_page(page)
    
    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)