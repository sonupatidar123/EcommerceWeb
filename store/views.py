from django.shortcuts import render, get_object_or_404
from .models import Product
from Category.models import Category 
from cart.models import Cartitem
from cart.views import _cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def store(request, category_slug=None):
    category = None
    products = None

    if category_slug:   # if slug is given
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:               # if no slug → show all
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)


    

        product_count = products.count()

    context = { 
        'products':   paged_products ,
        'product_count': product_count

    }
    return render(request, 'store/store.html', context)
def product_detail(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart =Cartitem.objects.filter(cart__cart_id= _cart_id(request),product=single_product).exists()


        
        
    except Exception as e:
        raise e
    
    context={
        'single_product':single_product,
        'in_cart':in_cart
    }
    
    return render(request,'store/product_detail.html',context)

def search(request):
    return render(request,'store/store.html')