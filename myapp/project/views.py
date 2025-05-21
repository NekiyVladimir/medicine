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
from django.contrib.auth.models import User, Group
from django.db.models import Count
from .models import News, Block, Tasks, Tickets, Employee, Organization, InternalDocs, Documents, Event
from django.contrib import messages
from django.forms import modelformset_factory


def index(request):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'index.html', {'username': username, 'group': group})


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
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    return render(request, 'document_detail.html', {'document': document, 'blocks': blocks,
                                                    'group': group})


def news(request):
    username = request.user.username if request.user.is_authenticated else ''
    news_list = News.objects.all()
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    return render(request, 'news.html', {'username': username, 'news': news_list, 'group': group})


def news_detail(request, news_id):
    username = request.user.username if request.user.is_authenticated else ''
    news_item = get_object_or_404(News, id=news_id)
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    return render(request, 'news_detail.html', {'username': username, 'news_item': news_item,
                                                'group': group})


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
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    return render(request, 'my_tasks.html', {'username': username, 'tasks': tasks_list,
                                             'group': group})


@login_required
def tasks_detail(request, tasks_id):
    username = request.user.username if request.user.is_authenticated else ''
    tasks_item = get_object_or_404(Tasks, id=tasks_id)
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    return render(request, 'tasks_detail.html', {'username': username, 'tasks_item': tasks_item,
                                                 'group': group})


@login_required
def create_news(request):
    username = request.user.username if request.user.is_authenticated else ''
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)  # Обработка формы с файлами
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # Устанавливаем автора
            article.save()
            return redirect('news')
    else:
        form = NewsForm()

    return render(request, 'create-news.html', {'form': form, 'username': username, 'group': group})


@login_required
def create_tasks(request):
    username = request.user.username if request.user.is_authenticated else ''
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
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

    return render(request, 'create_task.html', {'form': form, 'username': username, 'group': group})


@login_required
def internal_docs(request):
    username = request.user.username if request.user.is_authenticated else ''
    docs = InternalDocs.objects.all()
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    return render(request, 'internal_docs.html', {'username': username, 'docs': docs, 'group': group})


@login_required
def docs_detail(request, doc_id):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    username = request.user.username if request.user.is_authenticated else ''
    docs_item = get_object_or_404(InternalDocs, id=doc_id)
    return render(request, 'doc.html', {'username': username, 'docs_item': docs_item, 'group': group})


@login_required
def docs_add(request):
    username = request.user.username if request.user.is_authenticated else ''
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    if request.method == 'POST':
        form = InternalDocsForm(request.POST, request.FILES)  # Обработка формы с файлами
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # Устанавливаем автора
            article.save()
            return redirect('internal_docs')
    else:
        form = InternalDocsForm()

    return render(request, 'docs_add.html', {'form': form, 'username': username, 'group': group})


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
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    tickets_list = Tickets.objects.filter(author=request.user)
    return render(request, 'my_tickets.html', {'username': username, 'tasks': tickets_list,
                                               'group': group})


@login_required
def create_tickets(request):
    username = request.user.username if request.user.is_authenticated else ''
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
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

    return render(request, 'create_tickets.html', {'form': form, 'username': username,
                                                   'group': group})


@login_required
def add_comment_ticket(request, tickets_id):
    username = request.user.username if request.user.is_authenticated else ''
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    tickets_item = get_object_or_404(Tickets, id=tickets_id)
    if request.method == 'POST':
        form = TicketCommentForm(request.POST, instance=tickets_item)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.employee = request.user
            ticket.save()
            return redirect('tickets_detail', tickets_id=tickets_item.id)
    else:
        form = TicketCommentForm(instance=tickets_item)

    return render(request, 'add_comment_ticket.html', {'form': form, 'tickets_item': tickets_item,
                                                       'username': username, 'group': group})


def register(request):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
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
    return render(request, 'register.html', {'form': form, 'group': group})


def employee_register(request):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('index')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'employee_register.html', {'form': form, 'group': group})


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
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    if request.method == 'POST':
        form = OrganizationRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('index')
    else:
        form = OrganizationRegistrationForm()
    return render(request, 'organization_register.html', {'form': form, 'group': group})


def login_view(request):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form, 'group': group})


@login_required
def create_document(request):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
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
            # images = request.FILES.getlist('image')
            # videos = request.FILES.getlist('video')
            images = []
            videos = []

            for i in range(1, len(block_types) + 1):  # Перебираем все блоки
                image = request.FILES.get(f'image_{i}')
                video = request.FILES.get(f'video_{i}')

                # Добавляем в списки, если они существуют, или None
                images.append(image if image else '')
                videos.append(video if video else '')

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

    return render(request, 'create_document.html', {'document_form': document_form, 'group': group})


@login_required
def delete_news(request, new_id):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    news_item = get_object_or_404(News, id=new_id)

    if request.method == 'POST':
        news_item.delete()
        return redirect('news')

    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'news_detail.html', {'username': username, 'news_item': news_item,
                                                'group': group})


@login_required
def delete_task(request, task_id):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    task_item = get_object_or_404(Tasks, id=task_id)

    if request.method == 'POST':
        task_item.delete()
        return redirect('tasks')

    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'tasks_detail.html', {'username': username, 'task_item': task_item,
                                                 'group': group})


@login_required
def delete_ticket(request, ticket_id):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    ticket_item = get_object_or_404(Tickets, id=ticket_id)

    if request.method == 'POST':
        ticket_item.delete()
        return redirect('tickets')

    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'tickets_detail.html', {'username': username, 'tickets_item': ticket_item,
                                                   'group': group})


@login_required
def delete_doc(request, doc_id):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    docs_item = get_object_or_404(InternalDocs, id=doc_id)

    if request.method == 'POST':
        docs_item.delete()
        return redirect('internal_docs')

    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'tickets_detail.html', {'username': username, 'docs_item': docs_item,
                                                   'group': group})


@login_required
def delete_document(request, document_id):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    document = get_object_or_404(Documents, id=document_id)
    blocks = document.blocks.all()

    if request.method == 'POST':
        document.delete()
        return redirect('documents')

    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'tickets_detail.html', {'username': username, 'document': document,
                                                   'blocks': blocks, 'group': group})


@login_required
def calendar(request):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    events = Event.objects.all()
    return render(request, 'calendar.html', {'events': events, 'group': group})


@login_required
def reports(request):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    # Получаем группу "Сотрудник"
    employee_group = Group.objects.get(name='Сотрудник')

    # Получаем всех пользователей из группы "Сотрудник" и считаем количество связанных документов, статей и постов
    employees = User.objects.filter(groups=employee_group).annotate(
        document_count=Count('document', distinct=True),
        new_count=Count('news', distinct=True),
        task_count=Count('task', distinct=True),
        ticket_count=Count('ticket_employee', distinct=True),
        doc_count=Count('docs', distinct=True),
    )
    for employee in employees:
        print(employee.new_count)
        print(employee.doc_count)

    # Подготовка данных для диаграммы
    labels = [employee.first_name for employee in employees]
    document_counts = [employee.document_count for employee in employees]
    new_counts = [employee.new_count for employee in employees]
    task_counts = [employee.task_count for employee in employees]
    ticket_counts = [employee.ticket_count for employee in employees]
    doc_counts = [employee.doc_count for employee in employees]

    context = {
        'labels': labels,
        'document_counts': document_counts,
        'new_counts': new_counts,
        'task_counts': task_counts,
        'ticket_counts': ticket_counts,
        'doc_counts': doc_counts,
        'group': group,
    }
    return render(request, 'reports.html', context)


@login_required
def update_documents(request, document_id):
    groups = request.user.groups.first()  # Получаем все группы пользователя
    group = groups.name if groups else None
    document = get_object_or_404(Documents, id=document_id)

    if request.method == 'POST':
        document_form = DocumentForm(request.POST, instance=document)
        if document_form.is_valid():
            document = document_form.save(commit=False)
            document.updated_by = request.user  # Устанавливаем обновляющего
            document.save()

            # Обработка блоков
            block_orders = request.POST.getlist('old_order')
            new_orders = request.POST.getlist('new_order')
            block_types = request.POST.getlist('block_type')
            contents = request.POST.getlist('content')
            images = []
            videos = []

            for i in range(len(block_types)):
                image = request.FILES.get(f'image_{i}')
                video = request.FILES.get(f'video_{i}')

                # Добавляем в списки, если они существуют, или None
                images.append(image if image else '')
                videos.append(video if video else '')
            for block in document.blocks.all():
                if str(block.order) in block_orders:
                    print('OK')
                else:
                    block.delete()
            for i in range(len(new_orders)):
                if new_orders[i] == block_orders[i]:
                    block = document.blocks.get(order=int(new_orders[i]))
                    block.block_type = block_types[i]
                    block.content = contents[i]
                    block.order = new_orders[i]
                    if images[i]:
                        block.image = images[i]
                    if videos[i]:
                        block.video = videos[i]
                    block.save()
                elif block_orders[i] != 'new':
                    block_old = document.blocks.get(order=int(block_orders[i]))
                    block_old.block_type = block_types[i]
                    block_old.content = contents[i]
                    block_old.order = int(new_orders[i])+1000
                    if images[i]:
                        block_old.image = images[i]
                    if videos[i]:
                        block_old.video = videos[i]
                    block_old.save()
                else:
                    block = Block(
                        document=document,
                        block_type=block_types[i],
                        content=contents[i],
                        image=images[i],
                        video=videos[i],
                        order=new_orders[i],
                    )
                    block.save()
            for block in document.blocks.all():
                if block.order > 999:
                    block.order = block.order - 1000
                    block.save()

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
            'id': block.id  # Добавляем ID блока для обработки
        })

    return render(request, 'update_documents.html', {
        'document_form': document_form,
        'block_forms': block_forms,
        'document': document,
        'group': group,
    })

    # document = get_object_or_404(Documents, id=document_id)
    #
    # if request.method == 'POST':
    #     document_form = DocumentForm(request.POST, instance=document)
    #     if document_form.is_valid():
    #         document = document_form.save(commit=False)
    #         document.updated_by = request.user  # Устанавливаем обновляющего
    #         document.save()
    #
    #         # Обработка блоков
    #         block_types = request.POST.getlist('block_type')
    #         contents = request.POST.getlist('content')
    #         images = request.FILES.getlist('image')  # Получаем список изображений
    #         videos = request.FILES.getlist('video')  # Получаем список видео
    #
    #         existing_block_ids = [block.id for block in document.blocks.all()]  # Существующие блоки
    #         new_block_ids = []  # Список для новых блоков
    #
    #         for i in range(len(block_types)):
    #             if i < len(existing_block_ids):
    #                 # Обновляем существующий блок
    #                 block = Block.objects.get(id=existing_block_ids[i])
    #                 block.block_type = block_types[i]  # Обновляем тип блока
    #                 block.content = contents[i]  # Обновляем контент
    #
    #                 # Сохраняем файлы только если тип блока соответствует
    #                 if block_types[i] == "Изображение":
    #                     if i < len(images) and images[i]:  # Проверяем, что файл загружен
    #                         block.image = images[i]  # Обновляем изображение, если оно загружено
    #                 elif block_types[i] == "Видео":
    #                     if i < len(videos) and videos[i]:  # Проверяем, что файл загружен
    #                         block.video = videos[i]  # Обновляем видео, если оно загружено
    #
    #                 block.save()
    #                 new_block_ids.append(block.id)
    #             else:
    #                 # Создаем новый блок
    #                 block = Block(
    #                     document=document,
    #                     block_type=block_types[i],
    #                     content=contents[i],
    #                     image=images[i] if block_types[i] == "Изображение" and i < len(images) else None,
    #                     video=videos[i] if block_types[i] == "Видео" and i < len(videos) else None,
    #                 )
    #                 block.save()
    #                 new_block_ids.append(block.id)
    #
    #         # Удаляем блоки, которые больше не существуют в форме
    #         for block in document.blocks.exclude(id__in=new_block_ids):
    #             block.delete()
    #
    #         return redirect('documents')  # Перенаправление на страницу со списком документов
    # else:
    #     document_form = DocumentForm(instance=document)
    #
    # block_forms = []
    # for block in document.blocks.all():
    #     block_forms.append({
    #         'block_type': block.block_type,
    #         'content': block.content,
    #         'image': block.image,
    #         'video': block.video,
    #     })
    #
    # return render(request, 'update_documents.html', {
    #     'document_form': document_form,
    #     'block_forms': block_forms,
    #     'document': document,
    # })



