from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Cartitem
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist

def _cart_id(request):

    """Get the session key for the cart. If no session exists, create a new one."""
   
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart(request, product_id):

    # Get the product
    product = get_object_or_404(Product , id=product_id)
    # Get or create cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    #  Get or create cart item
    try:
        cart_item = Cartitem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1   # increase quantity
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item = Cartitem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        # no need to call .save(), create() already saves
        cart_item.save()
    

    return redirect('cart')

def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cartitem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()


    return redirect('cart')


def remove_cart_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cartitem.objects.get(product=product,cart=cart)
    cart_item.delete()

    return redirect('cart')


def cart(request,total=0,quantity=0,cart_items=None):
    tax=0
    grant_total=0
    cart_items=None
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=Cartitem.objects.filter(cart=cart, is_active=True)

      
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax =(2*total)/100
        grand_total =total + tax
    except ObjectDoesNotExist:
        pass # just ignore
 
    context= {
        'total' : total ,
        'quantity': quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }

    
    return render(request, 'store/cart.html',context)

