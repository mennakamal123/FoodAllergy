from django.contrib import admin
from . import models
from .models import Product, Cart,CartItem, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
 
    search_fields = [
        "arabicName",
        "englishName",
        "arabicDescription",
        "englishDescription",
    ]

    filterset_fields = [
        "arabicName",
        "englishName",
        "arabicDescription",
        "englishDescription",
    ]
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)

