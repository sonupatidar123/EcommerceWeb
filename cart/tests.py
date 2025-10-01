from django.test import TestCase, Client
from django.urls import reverse
from .models import Cart, Cartitem
from store.models import Product
from .views import _cart_id
from .context_processor import counter

class CartModelTest(TestCase):
    def setUp(self):
        self.cart = Cart.objects.create(cart_id='test123')
        self.product = Product.objects.create(
            product_name='Test Product',
            slug='test-product',
            description='desc',
            price=50,
            images='photos/products/test.jpg',
            stock=5,
            is_available=True,
            category_id=1
        )
        self.cart_item = Cartitem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
            is_active=True
        )

    def test_cart_str(self):
        self.assertEqual(str(self.cart), self.cart.cart_id)

    def test_cartitem_str(self):
        self.assertEqual(str(self.cart_item), self.product.product_name)

class CartViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cart = Cart.objects.create(cart_id='test123')
        self.product = Product.objects.create(
            product_name='Test Product',
            slug='test-product',
            description='desc',
            price=50,
            images='photos/products/test.jpg',
            stock=5,
            is_available=True,
            category_id=1
        )
        self.cart_item = Cartitem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
            is_active=True
        )

    def test_cart_view(self):
        session = self.client.session
        session['cart_id'] = self.cart.cart_id
        session.save()
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')
        self.assertIn('cart_items', response.context)

class CartContextProcessorTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cart = Cart.objects.create(cart_id='test123')
        self.product = Product.objects.create(
            product_name='Test Product',
            slug='test-product',
            description='desc',
            price=50,
            images='photos/products/test.jpg',
            stock=5,
            is_available=True,
            category_id=1
        )
        Cartitem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
            is_active=True
        )

    def test_counter(self):
        request = self.client.request().wsgi_request
        request.session['cart_id'] = self.cart.cart_id
        result = counter(request)
        self.assertIn('cart_count', result)
        self.assertEqual(result['cart_count'], 2)
