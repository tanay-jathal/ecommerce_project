from django.test import TestCase
from shop.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_create_product(self):
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        product = Product.objects.create(
            name="Test Product",
            description="A test product",
            price=Decimal('99.99'),
            image=image,
            stock=10,
            in_stock=True,
            category=self.category
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, Decimal('99.99'))
        self.assertTrue(product.in_stock)
