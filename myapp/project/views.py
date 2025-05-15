from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import requests
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm, NewsForm, BlockForm, TasksForm, TicketsForm, \
    EmployeeRegistrationForm, OrganizationRegistrationForm, EmployeeProfileForm, InternalDocsForm, TicketCommentForm, \
    DocumentForm
from .models import News, Block, Tasks, Tickets, Employee, Organization, InternalDocs, Documents, Event
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
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    documents = Documents.objects.all()
    return render(request, 'documents.html', {'username': username, 'group': group,
                                              'documents': documents})


@login_required
def document_detail(request, document_id):
    document = get_object_or_404(Documents, id=document_id)
    blocks = document.blocks.all()
    return render(request, 'document_detail.html', {'document': document, 'blocks': blocks})


def news(request):
    username = request.user.username if request.user.is_authenticated else ''
    news_list = News.objects.all()
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    return render(request, 'news.html', {'username': username, 'news': news_list, 'group': group})


def news_detail(request, news_id):
    username = request.user.username if request.user.is_authenticated else ''
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'username': username, 'news_item': news_item})


@login_required
def tasks(request):
    username = request.user.username if request.user.is_authenticated else ''
    tasks_list = Tasks.objects.all()
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    return render(request, 'tasks.html', {'username': username, 'tasks': tasks_list, 'group': group})


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
            api_url = "https://edoctordocs.mantishub.io/api/rest/issues"
            api_token = "U5O5_TBiKZ2RFqsLzsFVBTuq-Lh4rr1T"

            headers = {
                "Authorization": api_token,
                "Content-Type": "application/json"
            }

            # Подготовка данных для MantisBT
            payload = {
                "summary": article.title,
                "description": article.description,
                "project": {
                    "id": "1"
                },
                "category": {
                    "id": 2,
                    "name": "test"
                },
                "priority": {
                    "id": "30",  # Замените на нужный приоритет
                    "name": "normal"
                },
                "status": {
                    "id": "30"  # Замените на нужный статус
                },
                #"custom_fields": [
                    #{
                    #    "field": "Urgency",
                    #    "value": article.urgency
                    #},
                    #{
                    #    "field": "Customer",
                    #    "value": article.customer
                    #},
                    #{
                    #    "field": "Assignee",
                    #    "value": article.assignee.name
                    #},
                    #{
                     #   "field": "Deadline",
                     #   "value": article.deadline.isoformat()  # Преобразование даты в строку
                    #}
                #]
            }

            # Выполнение POST-запроса к MantisBT
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))

            if response.status_code == 201:
                print('Задача успешно создана в MantisBT')
            else:
                print('Ошибка при создании задачи в MantisBT:', response.text)

            return redirect('tasks')
    else:
        form = TasksForm()

    return render(request, 'create_task.html', {'form': form, 'username': username})


@login_required
def internal_docs(request):
    username = request.user.username if request.user.is_authenticated else ''
    docs = InternalDocs.objects.all()
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    return render(request, 'internal_docs.html', {'username': username, 'docs': docs, 'group': group})


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
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    tickets_list = Tickets.objects.all()
    return render(request, 'tickets.html', {'username': username, 'tickets': tickets_list,
                                            'group': group})


@login_required
def tickets_detail(request, tickets_id):
    username = request.user.username if request.user.is_authenticated else ''
    tickets_item = get_object_or_404(Tickets, id=tickets_id)
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    return render(request, 'tickets_detail.html', {'username': username,
                                                   'tickets_item': tickets_item, 'group': group})


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
            article.customer = organization.name
            article.author = request.user
            article.save()
            return redirect('tickets')
    else:
        form = TicketsForm()

    return render(request, 'create_tickets.html', {'form': form, 'username': username})


@login_required
def add_comment_ticket(request, tickets_id):
    username = request.user.username if request.user.is_authenticated else ''
    tickets_item = get_object_or_404(Tickets, id=tickets_id)
    if request.method == 'POST':
        form = TicketCommentForm(request.POST, instance=tickets_item)
        if form.is_valid():
            form.save()
            return redirect('tickets_detail', tickets_id=tickets_item.id)
    else:
        form = TicketCommentForm(instance=tickets_item)

    return render(request, 'add_comment_ticket.html', {'form': form, 'tickets_item': tickets_item,
                                                       'username': username})


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
    if request.method == 'POST':
        document_form = DocumentForm(request.POST)
        if document_form.is_valid():
            document = document_form.save(commit=False)
            document.author = request.user  # Установите автора
            document.updated_by = request.user  # Установите обновляющего
            document.save()

            # Обработка блоков
            block_types = request.POST.getlist('block_type')
            contents = request.POST.getlist('content')
            images = request.FILES.getlist('image')
            videos = request.FILES.getlist('video')

            for i in range(len(block_types)):
                block = Block(
                    document=document,
                    block_type=block_types[i],
                    content=contents[i],
                    image=images[i] if i < len(images) else None,
                    video=videos[i] if i < len(videos) else None,
                    order=i
                )
                block.save()

            return redirect('documents')  # Перенаправление на страницу со списком документов
    else:
        document_form = DocumentForm()

    return render(request, 'create_document.html', {'document_form': document_form})


@login_required
def delete_news(request, new_id):
    news_item = get_object_or_404(News, id=new_id)

    if request.method == 'POST':
        news_item.delete()
        return redirect('news')

    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'news_detail.html', {'username': username, 'news_item': news_item})


@login_required
def delete_task(request, task_id):
    task_item = get_object_or_404(Tasks, id=task_id)

    if request.method == 'POST':
        task_item.delete()
        return redirect('tasks')

    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'tasks_detail.html', {'username': username, 'task_item': task_item})


@login_required
def delete_ticket(request, ticket_id):
    ticket_item = get_object_or_404(Tickets, id=ticket_id)

    if request.method == 'POST':
        ticket_item.delete()
        return redirect('tickets')

    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'tickets_detail.html', {'username': username, 'tickets_item': ticket_item})


@login_required
def delete_doc(request, doc_id):
    docs_item = get_object_or_404(InternalDocs, id=doc_id)

    if request.method == 'POST':
        docs_item.delete()
        return redirect('internal_docs')

    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'tickets_detail.html', {'username': username, 'docs_item': docs_item})


@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Documents, id=document_id)
    blocks = document.blocks.all()

    if request.method == 'POST':
        document.delete()
        return redirect('documents')

    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'tickets_detail.html', {'username': username, 'document': document,
                                                   'blocks': blocks})


@login_required
def calendar(request):
    events = Event.objects.all()
    return render(request, 'calendar.html', {'events': events})


@login_required
def update_documents(request, document_id):
    document = get_object_or_404(Documents, id=document_id)

    if request.method == 'POST':
        document_form = DocumentForm(request.POST, instance=document)
        if document_form.is_valid():
            document = document_form.save(commit=False)
            document.updated_by = request.user  # Устанавливаем обновляющего
            document.save()

            # Обработка блоков
            block_types = request.POST.getlist('block_type')
            contents = request.POST.getlist('content')
            images = request.FILES.getlist('image')  # Получаем список изображений
            print(images)
            videos = request.FILES.getlist('video')  # Получаем список видео

            existing_block_ids = [block.id for block in document.blocks.all()]
            new_block_ids = []

            for i in range(len(block_types)):
                if i < len(existing_block_ids):
                    # Обновляем существующий блок
                    block = Block.objects.get(id=existing_block_ids[i])
                    block.block_type = block_types[i]
                    block.content = contents[i]

                    # Сохраняем файлы только если тип блока соответствует
                    if block_types[i] == "Изображение":
                        block.image = images[i] if i < len(
                            images) else block.image  # Сохраняем новое изображение или оставляем старое
                    elif block_types[i] == "Видео":
                        block.video = videos[i] if i < len(
                            videos) else block.video  # Сохраняем новое видео или оставляем старое

                    block.save()
                    new_block_ids.append(block.id)
                else:
                    # Создаем новый блок
                    block = Block(
                        document=document,
                        block_type=block_types[i],
                        content=contents[i],
                        image=images[i] if block_types[i] == "Изображение" else None,
                        video=videos[i] if block_types[i] == "Видео" else None,
                        order=i
                    )
                    block.save()
                    new_block_ids.append(block.id)

            # Удаляем блоки, которые больше не существуют в форме
            for block in document.blocks.exclude(id__in=new_block_ids):
                block.delete()

            return redirect('documents')  # Перенаправление на страницу со списком документов
    else:
        document_form = DocumentForm(instance=document)

    block_forms = []
    for block in document.blocks.all():
        block_forms.append({
            'block_type': block.block_type,
            'content': block.content,
            'image': block.image,
            'video': block.video,
        })

    return render(request, 'update_documents.html', {
        'document_form': document_form,
        'block_forms': block_forms,
        'document': document,
    })



