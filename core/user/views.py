from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.context_processors import request

from .forms import RegistrationForm

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!  ')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')

            return render(request, 'user/register.html', {'form': form})

    form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        user_email = request.POST['email']
        user_password = request.POST['password']
        user = authenticate(request, username=user_email, password=user_password)

        if user:
            login(request, user)
            messages.success(request, f'Вы вошли как {request.user}')
            return redirect('home_page')
        messages.error(request, 'Неверный логин или пароль! ')

    return render(request, 'user/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('home_page')