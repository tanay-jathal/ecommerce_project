from django.test import TestCase
from django.urls import reverse
from shop.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal

class ProductListViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        Product.objects.create(
            name="Test Product",
            description="Description here",
            price=Decimal('100.00'),
            image=image,
            stock=5,
            in_stock=True,
            category=self.category
        )

    def test_product_list_view(self):
        url = reverse('product_list')  # ensure this is defined in your urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
