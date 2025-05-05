from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from .models import News, Document, Block
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='Группа')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'group']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class NewsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label='Текст новости')

    class Meta:
        model = News
        fields = ['title', 'content', 'file']

        labels = {
            'title': 'Заголовок',
            'content': 'Текст новости',
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


