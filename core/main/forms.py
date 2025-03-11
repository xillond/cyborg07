from django import forms
from .models import Product, Image


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'is_active']

