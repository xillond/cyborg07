from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class RegistrationForm(UserCreationForm):


    class Meta:
        model = MyUser
        fields = ('first_name', 'email', 'phone_number')
