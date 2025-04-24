from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm


def index(request):
    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'index.html', {'username': username})


@login_required
def documents(request):
    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'documents.html', {'username': username})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']
            group.user_set.add(user)  # Добавляем пользователя в выбранную группу
            login(request, user)  # Автоматически аутентифицируем пользователя после регистрации
            return redirect('index')  # Измените на ваш URL
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Измените на ваш URL
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})