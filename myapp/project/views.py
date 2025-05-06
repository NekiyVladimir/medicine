from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm, NewsForm, DocumentForm, BlockForm, TasksForm, TicketsForm
from .models import News, Document, Block, Tasks, Tickets
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


def news_detail(request, news_id):
    username = request.user.username if request.user.is_authenticated else ''
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'username': username, 'news_item': news_item})


@login_required
def tasks(request):
    username = request.user.username if request.user.is_authenticated else ''
    tasks_list = Tasks.objects.all()
    return render(request, 'tasks.html', {'username': username, 'tasks': tasks_list})


@login_required
def tasks_detail(request, tasks_id):
    username = request.user.username if request.user.is_authenticated else ''
    tasks_item = get_object_or_404(Tasks, id=tasks_id)
    return render(request, 'tasks_detail.html', {'username': username, 'tasks_item': tasks_item})


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

    return render(request, 'create-news.html', {'form': form, 'username': username})


@login_required
def create_tasks(request):
    username = request.user.username if request.user.is_authenticated else ''
    if request.method == 'POST':
        form = TasksForm(request.POST, request.FILES)  # Обработка формы с файлами
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # Устанавливаем автора
            article.save()
            return redirect('tasks')  # Перенаправление на страницу списка новостей
    else:
        form = TasksForm()

    return render(request, 'create_task.html', {'form': form, 'username': username})


@login_required
def tickets(request):
    username = request.user.username if request.user.is_authenticated else ''
    tickets_list = Tickets.objects.all()
    return render(request, 'tickets.html', {'username': username, 'tickets': tickets_list})


@login_required
def tickets_detail(request, tickets_id):
    username = request.user.username if request.user.is_authenticated else ''
    tickets_item = get_object_or_404(Tasks, id=tickets_id)
    return render(request, 'tickets_detail.html', {'username': username, 'tickets_item': tickets_item})


@login_required
def create_tickets(request):
    username = request.user.username if request.user.is_authenticated else ''
    if request.method == 'POST':
        form = TicketsForm(request.POST, request.FILES)  # Обработка формы с файлами
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('tickets')  # Перенаправление на страницу списка новостей
    else:
        form = TicketsForm()

    return render(request, 'create_tickets.html', {'form': form, 'username': username})


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
