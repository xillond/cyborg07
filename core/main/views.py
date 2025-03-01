from unicodedata import category

from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Image

User = get_user_model()

def home_page(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'main/index.html', {'products': products})


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()
    similar_products = Product.objects.filter(category=product.category.id).exclude(id=product.id)[:8]
    return render(request=request,
                  template_name='main/product_details.html',
                  context={'product': product, 'images': images, 'similar_products': similar_products}
                  )

def all_products_in_category(request, category_id):
    products = Product.objects.filter(category=category_id)
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'main/all_in_category.html',{'products': products, 'category': category})


def profile_page(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_products = user.products.all().order_by('-is_active')
    return render(
        request=request,
        template_name='main/profile.html',
        context={'user': user, 'user_products': user_products}
    )
