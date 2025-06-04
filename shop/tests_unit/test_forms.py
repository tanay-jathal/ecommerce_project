from django.test import TestCase
from django.contrib.auth.models import User
from shop.forms import ProductForm, RegisterForm
from shop.models import Category
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from PIL import Image
import io

def get_test_image_file():
    # Create a simple 100x100 red image in memory
    image = Image.new('RGB', (100, 100), color='red')
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='JPEG')
    byte_arr.seek(0)
    return SimpleUploadedFile('test.jpg', byte_arr.read(), content_type='image/jpeg')

class ProductFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_valid_product_form(self):
        image = get_test_image_file()
        form_data = {
            'name': 'Sample Product',
            'description': 'Product description',
            'price': Decimal('120.50'),
            'stock': 15,
            'category': self.category.id,
        }
        form_files = {'image': image}
        form = ProductForm(data=form_data, files=form_files)
        if not form.is_valid():
            print("ProductForm errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_product_form_missing_name(self):
        form_data = {
            'description': 'No name',
            'price': Decimal('120.50'),
            'stock': 15,
            'category': self.category.id,
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

class RegisterFormTest(TestCase):
    def test_valid_registration_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Password123',
            'password2': 'Password321',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_registration_form_missing_email(self):
        form_data = {
            'username': 'newuser',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
