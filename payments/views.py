# Create your views here.
import razorpay
import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from orders.models import Order, OrderProduct, Payment
from carts.models import CartItem
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import hmac
import hashlib

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def initiate_payment(request, order_id):
    """
    Initiate Razorpay payment for an order
    """
    try:
        order = Order.objects.get(order_number=order_id, user=request.user, is_ordered=False)
        amount = int(order.order_total * 100)  # amount in paisa
        currency = 'INR'

        # Create Razorpay order
        razorpay_order = client.order.create(dict(
            amount=amount,
            currency=currency,
            payment_capture='1',
            notes={
                'order_number': order.order_number,
                'user_email': request.user.email
            }
        ))

        context = {
            'order': order,
            'razorpay_order': razorpay_order,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount,
        }
        return render(request, 'orders/payments.html', context)
    except Order.DoesNotExist:
        return redirect('store')


@csrf_exempt
@require_http_methods(["POST"])
def payment_success(request):
    """
    Handle successful Razorpay payment and update order status

    """
    try:
        data = json.loads(request.body)
        
        # Extract payment details
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')
        order_number = data.get('order_id')

        # Verify Razorpay signature
        message = f'{razorpay_order_id}|{razorpay_payment_id}'
        expected_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

        if expected_signature != razorpay_signature:
            return JsonResponse({
                'success': False,
                'message': 'Payment signature verification failed'
            }, status=400)

        # Get order and verify it belongs to current user
        order = Order.objects.get(order_number=order_number, user=request.user, is_ordered=False)

        # Create Payment record
        payment = Payment(
            user=request.user,
            order=order,
            payment_id=razorpay_payment_id,
            payment_method='Razorpay',
            amount_paid=order.order_total,
            status='Completed'
        )
        payment.save()

        # Update order status
        order.payment = payment
        order.is_ordered = True
        order.save()

        # Move cart items to OrderProduct table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            # Handle product variations
            product_variation = item.variations.all()
            orderproduct.variations.set(product_variation)
            orderproduct.save()

            # Reduce product stock
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()

        # Send order confirmation email
        mail_subject = 'Order Confirmation - Thank you for your purchase!'
        message = render_to_string('orders/order_recieved_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        # Return success response with order details
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'payment_id': payment.payment_id,
            'message': 'Payment processed successfully'
        })

    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Payment processing error: {str(e)}'
        }, status=500)


@csrf_exempt
def payment_failed(request):
    """
    Handle failed payment
    """
    return JsonResponse({
        'success': False,
        'message': 'Payment failed. Please try again.'
    }, status=400)

