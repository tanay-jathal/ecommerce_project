from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  
    path('product/', views.product_list, name='product_list'),
    path('products/ajax-filter/', views.product_list, name='ajax_product_filter'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'), # updated here
    path('products/add/', views.product_create, name='product_add'),
    path('products/<int:pk>/edit/', views.product_update, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add-all-to-cart/', views.add_all_to_cart_view, name='add_all_to_cart'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist_view, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist_view, name='remove_from_wishlist'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.my_orders, name='order_list'),
    path('orders/<int:order_id>/invoice/', views.invoice_docx_view, name='invoice_docx'),
    path('orders/<int:order_id>/invoice/download/', views.download_invoice_docx, name='invoice_docx_download'),


    # Auth
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='product_list'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
