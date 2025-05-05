from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm, NewsForm, DocumentForm, BlockForm
from .models import News, Document, Block
from django.forms import modelformset_factory


def index(request):
    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'index.html', {'username': username})


@login_required
def profile(request):
    username = request.user.username if request.user.is_authenticated else ''
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    return render(request, 'profile.html', {'username': username, 'group': group})


@login_required
def documents(request):
    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'documents.html', {'username': username})


def news(request):
    username = request.user.username if request.user.is_authenticated else ''
    news_list = News.objects.all()
    return render(request, 'news.html', {'username': username, 'news': news_list})


@login_required
def create_news(request):
    username = request.user.username if request.user.is_authenticated else ''
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)  # Обработка формы с файлами
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # Устанавливаем автора
            article.save()
            return redirect('news')  # Перенаправление на страницу списка новостей
    else:
        form = NewsForm()

    return render(request, 'create-news.html', {'form': form, 'username': username})  # Отправляем форму в шаблон


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
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Измените на ваш URL
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def create_document(request):
    BlockFormSet = modelformset_factory(Block, form=BlockForm, extra=4)

    if request.method == 'POST':
        document_form = DocumentForm(request.POST)
        block_formset = BlockFormSet(request.POST, request.FILES, queryset=Block.objects.none())

        if document_form.is_valid() and block_formset.is_valid():
            document = document_form.save()
            blocks = block_formset.save(commit=False)
            for block in blocks:
                block.document = document
                block.save()
            return redirect('success_url')  # Замените на ваш URL

    else:
        document_form = DocumentForm()
        block_formset = BlockFormSet(queryset=Block.objects.none())

    return render(request, 'create_document.html', {
        'document_form': document_form,
        'block_formset': block_formset,
    })
