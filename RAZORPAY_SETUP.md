# Razorpay Payment Gateway Integration Guide

## Overview
This ecommerce platform now uses **Razorpay** as the payment gateway. Razorpay supports multiple payment methods including:
- Credit/Debit Cards
- UPI
- Wallets
- Net Banking
- And more

## Setup Instructions

### 1. Get Razorpay Credentials

1. Create an account on [Razorpay Dashboard](https://dashboard.razorpay.com)
2. Sign in and navigate to **Settings > API Keys**
3. Copy your:
   - **Key ID** (Publishable key)
   - **Key Secret** (Secret key)

### 2. Configure Environment Variables

Create or update your `.env` file in the project root:

```env
RAZORPAY_KEY_ID=your_key_id_here
RAZORPAY_KEY_SECRET=your_key_secret_here
```

**For production deployment on Heroku:**
```bash
heroku config:set RAZORPAY_KEY_ID=your_key_id_here
heroku config:set RAZORPAY_KEY_SECRET=your_key_secret_here
```

### 3. Run Migrations

Since the Payment model has been updated, run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Test the Integration

1. Create a test account in your app
2. Add products to cart
3. Proceed to checkout
4. Use Razorpay's test card: `4111 1111 1111 1111` with any future date and any CVV

## Payment Flow

```
1. User adds items to cart
   ↓
2. User proceeds to checkout
   ↓
3. User fills billing information
   ↓
4. Order created (not yet marked as paid)
   ↓
5. Redirected to payment initialization
   ↓
6. Razorpay payment form opens
   ↓
7. User completes payment
   ↓
8. Payment signature verified
   ↓
9. Order marked as paid, cart cleared
   ↓
10. Order confirmation email sent
   ↓
11. User redirected to order completion page
```

## File Changes

### Modified Files:
- **templates/orders/payments.html** - Removed PayPal code, implemented Razorpay checkout
- **payments/views.py** - Complete rewrite with Razorpay integration and signature verification
- **payments/urls.py** - Created with proper URL routing
- **payments/admin.py** - Enhanced admin interface for payment management
- **payments/models.py** - Updated with Razorpay-specific fields
- **orders/models.py** - Enhanced Payment model with better structure
- **orders/views.py** - Updated to redirect to payment gateway
- **EcommerceWeb/settings.py** - Added Razorpay configuration
- **EcommerceWeb/urls.py** - Added payments app URLs

### New Features:
- ✅ Signature verification for payment security
- ✅ Automatic order completion on successful payment
- ✅ Cart clearing after payment
- ✅ Order confirmation emails
- ✅ Stock reduction after order completion
- ✅ Payment status tracking in admin panel
- ✅ Complete payment audit trail

## Security Features

1. **Signature Verification**: Every payment is verified using HMAC-SHA256
2. **CSRF Protection**: All payment endpoints protected with CSRF tokens
3. **User Verification**: Payments only accepted for logged-in users
4. **Order Validation**: Order ownership verified before processing payment

## Troubleshooting

### Payment Gateway Not Loading
- Check if `RAZORPAY_KEY_ID` is set correctly
- Verify internet connection
- Check browser console for JavaScript errors

### Payment Not Processing
- Verify `RAZORPAY_KEY_SECRET` is correct
- Check Django logs for signature verification errors
- Ensure migrations have been run

### Admin Panel Not Showing Payments
- Run migrations: `python manage.py migrate`
- Restart Django server

## Testing Checklist

- [ ] Razorpay credentials configured
- [ ] Migrations run successfully
- [ ] Can access payment page
- [ ] Razorpay form loads
- [ ] Test payment completes
- [ ] Order marked as paid
- [ ] Cart cleared
- [ ] Confirmation email sent
- [ ] Payment visible in admin panel
- [ ] Order details accessible

## Support

For Razorpay API documentation, visit: https://razorpay.com/docs/

For payment issues, contact: https://support.razorpay.com/

## Demo Mode Removed

✓ All "This is a demo website" warnings have been removed
✓ PayPal integration code has been removed
✓ Ready for production payments
