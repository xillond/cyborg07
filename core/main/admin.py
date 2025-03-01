from django.contrib import admin
from .models import Category, Product, Image, Rating, Reply, Order, OrderItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Rating)
admin.site.register(Reply)
admin.site.register(Order)
admin.site.register(OrderItem)