from django.contrib import admin
from .models import UserLog, Product, Category, Order, OrderItem
from django.contrib.auth.models import User

# Register UserLog model for auditing purposes
@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'raw_password', 'created_at')
def get_username(self, obj):
    return obj.user.username if obj.user else 'No User'
get_username.short_description = 'Username'

# ProductAdmin to allow editing all fields for companyadmin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'price', 'stock', 'category']

    def get_readonly_fields(self, request, obj=None):
        # Do not restrict any fields for companyadmin
        if request.user.username == 'companyadmin':
            return []  # No readonly fields for companyadmin
        return super().get_readonly_fields(request, obj)

    def has_module_permission(self, request):
        # Allow access to the Product model for companyadmin
        return request.user.has_perm('shop.change_product')

# CategoryAdmin remains the same
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)

# Inline for OrderItem in OrderAdmin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

# OrderAdmin configuration (keeps it for superusers)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','username_display', 'email', 'created_at', 'total_price', 'products_with_quantities']
    inlines = [OrderItemInline]

    def username_display(self, obj):
        return obj.user.username if obj.user else '-'
    username_display.short_description = 'Username'

    def created_date(self, obj):
        return obj.created_at.date()  # This removes the time and returns only the date (YYYY-MM-DD)
    created_date.short_description = 'created_at'

    def total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())
    total_price.short_description = 'Total Price'

    def products_with_quantities(self, obj):
        return ", ".join([f"{item.product_name} (x{item.quantity})" for item in obj.items.all()])
    products_with_quantities.short_description = 'Products (Qty)'

# Register Order model as usual, no change required here
admin.site.register(Order, OrderAdmin)

