from django.db import models
from django.conf import settings
from store.models import Product, Variation

# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=200,blank=True)
    date_added=models.DateField(auto_now_add=True)


    def __str__(self):
         return self.cart_id
    

class CartItem(models.Model):
     product=models.ForeignKey(Product,on_delete=models.CASCADE)
     # link to user for authenticated carts; nullable to support anonymous session carts
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
     # session cart (nullable so items can belong to either a session cart or an authenticated user)
     cart=models.ForeignKey(Cart,on_delete=models.CASCADE, null=True, blank=True)
     quantity=models.IntegerField()
     variation =models.ManyToManyField(Variation,blank=True)
     is_active=models.BooleanField(default=True)
     def sub_total(self):
          return self.product.price * self.quantity
     def __str__(self):
          return f"{self.product.product_name} ({self.quantity})"
     def __unicode__(self):
          return str(self.product)

