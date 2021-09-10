from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import  get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models  import Category, CartProduct, Cart, Customer, Product
from .views import recalc_cart

User = get_user_model()


class ShopTestCases(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='password')
        self.category = Category.objects.create(name='Товары для животных', slug='petproducts')
        image = SimpleUploadedFile("product_image.jpg", content=b'', content_type="image/jpg")
        self.product = Product.objects.create(
            category=self.category,
            title='Test Product',
            slug='test-slug',
            image=image,
            price=Decimal('5000.00')
        )
        self.customer = Customer.objects.create(user=self.user, phone="375331233212", address="City")
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            product=self.product
        )

    def test_add_to_cart(self):
        self.cart.products.add(self.cart_product)
        recalc_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.products.count(), 1)
        self.assertEqual(self.cart.final_price, Decimal('5000.00'))