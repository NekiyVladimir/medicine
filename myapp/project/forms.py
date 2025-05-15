from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from .models import News, Block, Tasks, Tickets, Employee, EmployeePosition, Organization, InternalDocs, \
    Documents
from ckeditor.fields import RichTextField
from django.forms import inlineformset_factory
from ckeditor.widgets import CKEditorWidget


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='Группа')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'group']


class EmployeeRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True, label='Логин для авторизации')
    first_name = forms.CharField(max_length=30, required=True, label='Имя и Отчество')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    email = forms.EmailField(required=True, label='Электронная почта')
    phone = forms.CharField(max_length=15, required=False, label='Телефон')
    position = forms.ModelChoiceField(queryset=EmployeePosition.objects.all(), required=True, label='Должность')
    avatar = forms.ImageField(required=False, label='Аватарка')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Добавление пользователя в группу "Сотрудник"
            employee_group, created = Group.objects.get_or_create(name='Сотрудник')
            user.groups.add(employee_group)

            # Создание экземпляра Employee
            employee = Employee(
                user=user,
                phone=self.cleaned_data['phone'],
                position=self.cleaned_data['position'],
                avatar=self.cleaned_data['avatar']
            )
            employee.save()
        return user


class EmployeeProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Логин для авторизации')
    first_name = forms.CharField(max_length=150, label='Имя отчество')
    last_name = forms.CharField(max_length=150, label='Фамилия')
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput(), required=False,
                               label='Пароль (оставьте пустым, если не хотите менять)')

    class Meta:
        model = Employee
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'position', 'phone', 'avatar']
        widgets = {
            'position': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = user.username
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email

    def save(self, commit=True):
        employee = super().save(commit=False)
        user = employee.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            employee.save()
        return employee


class OrganizationRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True, label='Логин для авторизации')
    first_name = forms.CharField(max_length=30, required=True, label='Имя и Отчество')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    name = forms.CharField(max_length=100, required=True, label='Название организации')
    email = forms.EmailField(required=True, label='Электронная почта')
    phone = forms.CharField(max_length=15, required=False, label='Телефон')
    address = forms.CharField(max_length=200, required=False, label='Должность')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Добавление пользователя в группу "Организация"
            organization_group, created = Group.objects.get_or_create(name='Организация')
            user.groups.add(organization_group)

            # Создание экземпляра Organization
            organization = Organization(
                user=user,
                name=self.cleaned_data['name'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
            organization.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class NewsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label='Текст новости')

    class Meta:
        model = News
        fields = ['title', 'content', 'image']

        labels = {
            'title': 'Заголовок',
            'content': 'Текст новости',
            'image': 'Изображение',
        }


class TasksForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label='Текст задачи')

    class Meta:
        model = Tasks
        fields = ['title', 'description', 'file', 'urgency', 'priority', 'customer', 'assignee', 'deadline', 'status']

        labels = {
            'title': 'Заголовок',
            'description': 'Текст задачи',
            'file': 'Файл',
        }


class TicketsForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label='Текст обращения')

    class Meta:
        model = Tickets
        fields = ['title', 'description', 'file']

        labels = {
            'title': 'Тема обращения',
            'description': 'Текст обращения',
            'file': 'Файл',
        }


class TicketCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=CKEditorWidget(), label='Ответ к обращению')

    class Meta:
        model = Tickets
        fields = ['comment']

        labels = {
            'comment': 'Ответ к обращению',
        }


class InternalDocsForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label='Описание документа')

    class Meta:
        model = InternalDocs
        fields = ['title', 'description', 'type', 'file']

        labels = {
            'title': 'Название документа',
            'description': 'Описание документа',
            'type': 'Тип документа',
            'file': 'Файл',
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['title']


class BlockForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label='Текст документа', required=False)

    class Meta:
        model = Block
        fields = ['block_type', 'content', 'image', 'video']


