from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from .models import News, Document, Block, Tasks, Tickets, Employee, EmployeePosition, Organization
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='Группа')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'group']


class EmployeeRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    email = forms.EmailField(required=True, label='Электронная почта')
    phone = forms.CharField(max_length=15, required=False, label='Телефон')
    position = forms.ModelChoiceField(queryset=EmployeePosition.objects.all(), required=True, label='Должность')
    avatar = forms.ImageField(required=False, label='Аватарка')

    class Meta:
        model = User
        fields = ['username', 'last_name', 'email', 'password']

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


class OrganizationRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    name = forms.CharField(max_length=100, required=True, label='Название организации')
    email = forms.EmailField(required=True, label='Электронная почта')
    phone = forms.CharField(max_length=15, required=False, label='Телефон')
    address = forms.CharField(max_length=200, required=False, label='Должность')

    class Meta:
        model = User
        fields = ['username', 'last_name', 'email', 'password']

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
            'file': 'Файл',
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
        fields = ['title', 'description', 'file', 'customer']

        labels = {
            'title': 'Тема обращения',
            'description': 'Текст обращения',
            'file': 'Файл',
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title']


class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ['block_type', 'content', 'image', 'order']


