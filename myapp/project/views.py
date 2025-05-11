from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm, NewsForm, DocumentForm, BlockForm, TasksForm, TicketsForm, \
    EmployeeRegistrationForm, OrganizationRegistrationForm, EmployeeProfileForm, InternalDocsForm
from .models import News, Document, Block, Tasks, Tickets, Employee, Organization, InternalDocs
from django.contrib import messages
from django.forms import modelformset_factory


def index(request):
    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'index.html', {'username': username})


@login_required
def profile(request):
    username = request.user.first_name if request.user.is_authenticated else ''
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
def my_tasks(request):
    username = request.user.username if request.user.is_authenticated else ''
    tasks_list = Tasks.objects.filter(author=request.user)
    return render(request, 'my_tasks.html', {'username': username, 'tasks': tasks_list})


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
            return redirect('news')
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
            return redirect('tasks')
    else:
        form = TasksForm()

    return render(request, 'create_task.html', {'form': form, 'username': username})


@login_required
def internal_docs(request):
    username = request.user.username if request.user.is_authenticated else ''
    docs = InternalDocs.objects.all()
    return render(request, 'internal_docs.html', {'username': username, 'docs': docs})


@login_required
def docs_detail(request, doc_id):
    username = request.user.username if request.user.is_authenticated else ''
    docs_item = get_object_or_404(InternalDocs, id=doc_id)
    return render(request, 'doc.html', {'username': username, 'docs_item': docs_item})


@login_required
def docs_add(request):
    username = request.user.username if request.user.is_authenticated else ''
    if request.method == 'POST':
        form = InternalDocsForm(request.POST, request.FILES)  # Обработка формы с файлами
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # Устанавливаем автора
            article.save()
            return redirect('internal_docs')
    else:
        form = InternalDocsForm()

    return render(request, 'docs_add.html', {'form': form, 'username': username})


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
def my_tickets(request):
    username = request.user.username if request.user.is_authenticated else ''
    tickets_list = Tickets.objects.filter(author=request.user)
    return render(request, 'my_tickets.html', {'username': username, 'tasks': tickets_list})


@login_required
def create_tickets(request):
    username = request.user.username if request.user.is_authenticated else ''
    if request.method == 'POST':
        form = TicketsForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            organization = Organization.objects.get(user=request.user)
            article.customer = organization
            article.author = request.user
            article.save()
            return redirect('tickets')
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
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def employee_register(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('index')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'employee_register.html', {'form': form})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        employee = Employee.objects.get(user=request.user)
        form = EmployeeProfileForm(instance=employee, user=request.user)
        return render(request, 'edit_profile.html', {'form': form})

    def post(self, request):
        employee = Employee.objects.get(user=request.user)
        form = EmployeeProfileForm(request.POST, request.FILES, instance=employee, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'edit_profile.html', {'form': form})


def organization_register(request):
    if request.method == 'POST':
        form = OrganizationRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('index')
    else:
        form = OrganizationRegistrationForm()
    return render(request, 'organization_register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def create_document(request):
    BlockFormSet = modelformset_factory(Block, form=BlockForm, extra=4)
    username = request.user.username if request.user.is_authenticated else ''

    if request.method == 'POST':
        document_form = DocumentForm(request.POST)
        block_formset = BlockFormSet(request.POST, request.FILES, queryset=Block.objects.none())

        if document_form.is_valid() and block_formset.is_valid():
            document = document_form.save()
            blocks = block_formset.save(commit=False)
            for block in blocks:
                block.document = document
                block.save()
            return redirect('documents')

    else:
        document_form = DocumentForm()
        block_formset = BlockFormSet(queryset=Block.objects.none())

    return render(request, 'create_document.html', {'document_form': document_form,
        'block_formset': block_formset, 'username': username})
