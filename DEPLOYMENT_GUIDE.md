# 🚀 Deployment Quick Start

## 5-Step Deployment

### Step 1: Get Razorpay Credentials (2 min)
```
1. Go to https://dashboard.razorpay.com/app/settings/api-keys
2. Copy Key ID
3. Copy Key Secret
4. Done ✅
```

### Step 2: Set Environment Variables (1 min)

**For Local Development:**
```bash
echo "RAZORPAY_KEY_ID=rzp_test_xxx" >> .env
echo "RAZORPAY_KEY_SECRET=secret_xxx" >> .env
```

**For Heroku:**
```bash
heroku config:set RAZORPAY_KEY_ID=rzp_test_xxx
heroku config:set RAZORPAY_KEY_SECRET=secret_xxx
```

### Step 3: Run Migrations (1 min)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Test Locally (5 min)
```bash
python manage.py runserver
# Add items to cart → checkout → pay with test card
# Test card: 4111 1111 1111 1111
```

### Step 5: Deploy to Production (5 min)
```bash
# Update with live keys
heroku config:set RAZORPAY_KEY_ID=rzp_live_xxx
heroku config:set RAZORPAY_KEY_SECRET=live_secret_xxx

# Deploy
git push heroku main
```

**Total Time: ~15 minutes** ⏱️

---

## Test Cards

Use these to test payments:

```
Visa (Success):          4111 1111 1111 1111
Mastercard (Success):    5555 5555 5555 4444
International (Success): 4000 0576 5000 0290
Declined:                4000 0000 0000 0002
```

- Expiry: Any future date (e.g., 12/25)
- CVV: Any 3 digits (e.g., 123)

---

## Verification

### ✅ Local Testing
```bash
# 1. Start server
python manage.py runserver

# 2. Create test account
# 3. Add products to cart
# 4. Proceed to checkout
# 5. Pay with test card
# 6. Verify order marked as paid
# 7. Check admin for payment record
```

### ✅ Production Testing
```bash
# Use actual test cards (same as local)
# But with LIVE keys, you see sandbox transactions
# No real charges are made with test cards
```

### ✅ Admin Verification
```
Django Admin > Payments
Should see all payment records
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Keys not loading | Restart server after adding .env |
| Payment form blank | Check RAZORPAY_KEY_ID is set |
| Payment fails | Verify RAZORPAY_KEY_SECRET is correct |
| Order not marked as paid | Check migrations ran successfully |
| Payment not in admin | Run `python manage.py migrate` |

---

## What's Different Now

| Before | After |
|--------|-------|
| PayPal + Razorpay mix | **Razorpay only** |
| Demo warnings | **Removed** ✅ |
| No verification | **HMAC-SHA256 verification** |
| String currency fields | **Decimal fields** |
| No admin interface | **Full admin support** |

---

## Key Points

✅ **Single Payment Gateway** - Razorpay (supports 100+ payment methods)
✅ **No Demo Mode** - Production ready
✅ **Security** - Signature verification on every payment
✅ **Error Handling** - Comprehensive error messages
✅ **Admin Support** - Full payment management in Django admin

---

## Post-Deployment

### Monitor
- 📊 Razorpay dashboard for transactions
- 📧 Email notifications for orders
- 💾 Payment records in admin

### Maintain
- 🔐 Keep secrets secure
- 🔄 Regular backups
- 📋 Review payment reports

### Support
- 🆘 Razorpay: https://support.razorpay.com/
- 💬 Django docs: https://docs.djangoproject.com/

---

## Commands Cheat Sheet

```bash
# Setup
echo "RAZORPAY_KEY_ID=..." >> .env
python manage.py migrate

# Testing
python manage.py runserver
python manage.py test

# Admin
python manage.py createsuperuser
# Visit: http://localhost:8000/admin/

# Heroku
heroku config:set RAZORPAY_KEY_ID=...
git push heroku main
heroku logs --tail
```

---

## Common Issues & Fixes

### Keys not working?
```bash
# 1. Restart server
# 2. Check .env file syntax
# 3. Verify keys are correct (copy-paste carefully)
# 4. Check for extra spaces or quotes
```

### Payment modal not appearing?
```bash
# 1. Check browser console for errors
# 2. Verify RAZORPAY_KEY_ID is set
# 3. Check internet connection
# 4. Try incognito/private mode
```

### Order not marked as paid?
```bash
# 1. Check Django logs
# 2. Verify RAZORPAY_KEY_SECRET is correct
# 3. Run migrations: python manage.py migrate
# 4. Restart server
```

---

## Success Indicators

After deployment, you should see:

✅ Payment form loads with Razorpay button
✅ Payment processes successfully
✅ Order marked as "paid"
✅ Cart cleared
✅ Confirmation email sent
✅ Payment visible in admin
✅ No demo warnings

---

## Need Help?

1. **Read the docs**: Check RAZORPAY_SETUP.md
2. **Check the code**: See CODE_REFERENCE.md
3. **Compare versions**: See BEFORE_AFTER_COMPARISON.md
4. **Technical details**: See PAYMENT_INTEGRATION_CHANGES.md

---

## Timeline

| Step | Time | Status |
|------|------|--------|
| Get Razorpay account | 5-10 min | ⏳ |
| Add credentials | 1 min | ⏳ |
| Run migrations | 1 min | ⏳ |
| Test locally | 5-10 min | ⏳ |
| Deploy | 5 min | ⏳ |
| **Total** | **~20 min** | ⏳ |

---

**🎉 You're ready to go live!**

```
Payment Gateway: Razorpay ✅
Demo Mode: Removed ✅
Security: Verified ✅
Documentation: Complete ✅
Status: Production Ready 🚀
```

---

**Date**: February 2, 2026
**Ready for**: Live deployment
**Support**: 24/7 Razorpay support available
