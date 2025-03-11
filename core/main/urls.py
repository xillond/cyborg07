from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('category/<int:category_id>/', views.all_products_in_category, name='products_in_category'),
    path('user/<int:user_id>/', views.profile_page, name='profile_page'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/<int:product_id>/update/', views.update_product, name='update_product'),
    path('delete_image/', views.delete_image, name='delete_image'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('reply_review/<int:product_id>/', views.reply_review, name='reply_review'),
    path('edit_reply/<int:product_id>/', views.edit_reply, name='edit_reply'),
    path('delete_reply/<int:product_id>/', views.delete_reply, name='delete_reply'),
    path('cart/', views.cart_page, name='cart'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('payment/', views.payment_page, name='payment'),
    path('process_orders/', views.process_orders, name='process_orders'),
    path('update_cart/', views.update_cart_ajax, name='update_cart_ajax'),
    path('delete_cart_item/', views.delete_cart_item_ajax, name='delete_cart_item_ajax'),
    path('orders/', views.orders_page, name='orders'),
]
