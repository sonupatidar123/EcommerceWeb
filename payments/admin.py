from django.contrib import admin
from orders.models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'amount_paid', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('payment_id', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('payment_id', 'razorpay_signature', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'razorpay_order_id', 'razorpay_signature')
        }),
        ('User Details', {
            'fields': ('user',)
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'amount_paid', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# Note: Payment is already registered in orders.admin
# This admin class can be used by updating orders/admin.py if needed
