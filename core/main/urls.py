from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('category/<int:category_id>/', views.all_products_in_category, name='products_in_category'),
    path('user/<int:user_id>/', views.profile_page, name='profile_page')
]
