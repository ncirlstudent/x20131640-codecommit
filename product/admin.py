from django.contrib import admin
from product.models import Product, Category, Cart, BillingDetails, Order


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_name', 'slug',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'slug',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'purchased')
    
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cart_info', 'billing', 'status', 'payment_method')

    def get_cart_info(self, obj):
        return ", ".join([f"{cart.product} (Qty: {cart.quantity})" for cart in obj.carts.all()])

    get_cart_info.short_description = 'Cart Information'

admin.site.register(Order, OrderAdmin)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(BillingDetails)

