from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from shop.models import Product, Order, Category, OrderItem, WishlistItem, CartItem, UserLog
from django.contrib.auth import get_user_model
from django.contrib import messages
staff_required = user_passes_test(lambda u: u.is_staff)

@staff_required
def dashboard(request):
    return render(request, 'adminpanel/dashboard.html', {
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'total_users': User.objects.count(),
    })

@staff_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'adminpanel/product_list.html', {'products': products})

@staff_required
def order_list(request):
    orders = Order.objects.all()  # removed .select_related('user')
    return render(request, 'adminpanel/orders.html', {'orders': orders})

@staff_required
def user_list(request):
    users = User.objects.filter(is_staff=False)
    return render(request, 'adminpanel/users.html', {'users': users})


User = get_user_model()

@staff_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id, is_staff=False)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('user_list')

@staff_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id, is_staff=False)
    if request.method == "POST":
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('user_list')
    return render(request, "adminpanel/edit_user.html", {"user": user})

@staff_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Order deleted successfully.")
    return redirect('admin_order_list')

@staff_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.name = request.POST.get("name", order.name)
        order.email = request.POST.get("email", order.email)
        order.address = request.POST.get("address", order.address)
        order.phone = request.POST.get("phone", order.phone)
        order.save()
        messages.success(request, "Order updated successfully.")
        return redirect('order_list')
    return render(request, "adminpanel/edit_order.html", {"order": order})
