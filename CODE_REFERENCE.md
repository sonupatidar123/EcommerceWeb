# Code Reference: Razorpay Integration

## Environment Setup

### settings.py Configuration
```python
# Razorpay Payment Gateway Configuration
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID', default='')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET', default='')
```

### .env File
```
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

---

## Payment Views

### Initialize Payment
```python
def initiate_payment(request, order_id):
    """Start Razorpay payment for an order"""
    order = Order.objects.get(order_number=order_id, user=request.user, is_ordered=False)
    amount = int(order.order_total * 100)  # Convert to paisa
    
    razorpay_order = client.order.create(dict(
        amount=amount,
        currency='INR',
        payment_capture='1',
        notes={'order_number': order.order_number}
    ))
    
    return render(request, 'orders/payments.html', {
        'order': order,
        'razorpay_order': razorpay_order,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': amount,
    })
```

### Handle Payment Success
```python
@csrf_exempt
def payment_success(request):
    """Verify and process successful payment"""
    data = json.loads(request.body)
    
    # Verify signature
    message = f'{data["razorpay_order_id"]}|{data["razorpay_payment_id"]}'
    expected_signature = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    if expected_signature != data['razorpay_signature']:
        return JsonResponse({'success': False, 'message': 'Signature verification failed'})
    
    # Create payment record
    order = Order.objects.get(order_number=data['order_id'], user=request.user)
    payment = Payment.objects.create(
        user=request.user,
        order=order,
        payment_id=data['razorpay_payment_id'],
        razorpay_order_id=data['razorpay_order_id'],
        razorpay_signature=data['razorpay_signature'],
        payment_method='Razorpay',
        amount_paid=order.order_total,
        status='Completed'
    )
    
    # Update order and clear cart
    order.is_ordered = True
    order.save()
    CartItem.objects.filter(user=request.user).delete()
    
    return JsonResponse({'success': True, 'order_number': order.order_number})
```

---

## Frontend JavaScript

### Razorpay Checkout Form
```html
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<script>
document.getElementById('rzp-button1').onclick = function(e) {
    var options = {
        "key": "{{ razorpay_key_id }}",
        "amount": {{ amount }},
        "currency": "INR",
        "order_id": "{{ razorpay_order.id }}",
        "handler": function(response) {
            // Send to backend for verification
            fetch("{% url 'payment_success' %}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify({
                    razorpay_payment_id: response.razorpay_payment_id,
                    razorpay_order_id: response.razorpay_order_id,
                    razorpay_signature: response.razorpay_signature,
                    order_id: orderID
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "{% url 'order_complete' %}" + 
                        "?order_number=" + data.order_number + 
                        "&payment_id=" + data.payment_id;
                }
            });
        },
        "prefill": {
            "name": "{{ order.user.first_name }}",
            "email": "{{ order.user.email }}"
        },
        "theme": {"color": "#3399cc"}
    };
    
    var rzp = new Razorpay(options);
    rzp.on('payment.failed', function(response) {
        alert('Payment Failed: ' + response.error.description);
    });
    rzp.open();
};
</script>
```

---

## Models

### Payment Model
```python
class Payment(models.Model):
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True)
    payment_id = models.CharField(max_length=100, unique=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=200, blank=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.payment_id} - {self.status}'
```

---

## URL Routing

### payments/urls.py
```python
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/<str:order_id>/', views.initiate_payment, name='initiate_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
]
```

### Main urls.py (EcommerceWeb/)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),  # ← Added
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Admin Registration

### payments/admin.py
```python
from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'amount_paid', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('payment_id', 'user__email')
    readonly_fields = ('payment_id', 'razorpay_signature', 'created_at', 'updated_at')

admin.site.register(Payment, PaymentAdmin)
```

---

## Database Migration

```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Check status
python manage.py showmigrations
```

---

## Signature Verification Logic

```python
import hmac
import hashlib

# Create signature
message = f'{razorpay_order_id}|{razorpay_payment_id}'
expected_signature = hmac.new(
    settings.RAZORPAY_KEY_SECRET.encode(),
    message.encode(),
    hashlib.sha256
).hexdigest()

# Verify signature matches
is_valid = expected_signature == razorpay_signature
```

---

## Error Handling

```python
try:
    order = Order.objects.get(order_number=order_id, user=request.user)
except Order.DoesNotExist:
    return JsonResponse({
        'success': False,
        'message': 'Order not found'
    }, status=404)
except Exception as e:
    return JsonResponse({
        'success': False,
        'message': f'Error: {str(e)}'
    }, status=500)
```

---

## Testing Payments

```python
# Test payment with print statements
@csrf_exempt
def payment_success(request):
    data = json.loads(request.body)
    print(f"Payment ID: {data['razorpay_payment_id']}")
    print(f"Order ID: {data['razorpay_order_id']}")
    print(f"Signature: {data['razorpay_signature']}")
    # ... rest of code
```

---

**Ready for production! No more demo mode.** ✅
