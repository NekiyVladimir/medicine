# Generated by Django 4.2.20 on 2025-05-20 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Разработчик',
                'verbose_name_plural': 'Разработчики',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='EmployeePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название события')),
                ('description', models.TextField(blank=True, verbose_name='Описание события')),
                ('date', models.DateTimeField(verbose_name='Дата события')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Тема обращения')),
                ('description', models.TextField(verbose_name='Описание обращения')),
                ('customer', models.CharField(max_length=200, verbose_name='Заказчик (организация)')),
                ('file', models.FileField(blank=True, null=True, upload_to='tickets_files/', verbose_name='Файл')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания обращения')),
                ('status', models.CharField(choices=[('in_progress', 'В работе'), ('new', 'Новое'), ('decided', 'Решено')], default='new', max_length=15, verbose_name='Статус')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('author', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_employee', to=settings.AUTH_USER_MODEL, verbose_name='Ответ сотрудника')),
            ],
            options={
                'verbose_name': 'Обращение',
                'verbose_name_plural': 'Обращения',
                'ordering': ['-title'],
            },
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название задачи')),
                ('description', models.TextField(verbose_name='Описание задачи')),
                ('urgency', models.CharField(choices=[('low', 'Низкая'), ('medium', 'Средняя'), ('high', 'Высокая')], max_length=10, verbose_name='Срочность')),
                ('priority', models.CharField(choices=[('low', 'Низкий'), ('medium', 'Средний'), ('high', 'Высокий')], max_length=10, verbose_name='Приоритет')),
                ('customer', models.CharField(max_length=200, verbose_name='заказчик (организация)')),
                ('file', models.FileField(blank=True, null=True, upload_to='tasks_files/', verbose_name='Файл')),
                ('deadline', models.DateField(verbose_name='Дедлайн')),
                ('status', models.CharField(choices=[('in_progress', 'В работе'), ('completed', 'Выполнена'), ('under_review', 'На рассмотрении')], default='under_review', max_length=15, verbose_name='Статус')),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.developer', verbose_name='исполнитель')),
                ('author', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='task', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'ordering': ['-title'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название организации')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Адрес')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='телефон')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Текст новости')),
                ('image', models.ImageField(blank=True, null=True, upload_to='news_files/', verbose_name='Изображение')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата новости')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='InternalDocs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название документа')),
                ('description', models.TextField(verbose_name='Описание документа')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания вн. док.')),
                ('file', models.FileField(blank=True, null=True, upload_to='docs_files/', verbose_name='Файл')),
                ('type', models.CharField(choices=[('Приказ', 'Приказ'), ('Справка', 'Справка'), ('Заявление', 'Заявление')], max_length=15, verbose_name='Тип документа')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='docs', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Внутренний документ',
                'verbose_name_plural': 'Внутренние документы',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='телефон')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='аватарка')),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.employeeposition', verbose_name='Должность')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название документа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('version', models.DecimalField(decimal_places=1, default=1.0, max_digits=3, verbose_name='Версия документа')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document', to=settings.AUTH_USER_MODEL, verbose_name='ID пользователя, который создал')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_model_updaters', to=settings.AUTH_USER_MODEL, verbose_name='ID пользователя, который обновил')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_type', models.CharField(choices=[('Текст', 'Текст'), ('Изображение', 'Изображение'), ('Видео', 'Видео')], max_length=15)),
                ('content', models.TextField(blank=True, verbose_name='Текст документа')),
                ('image', models.ImageField(blank=True, upload_to='images/', verbose_name='Изображение')),
                ('video', models.FileField(blank=True, upload_to='video/', verbose_name='Видео')),
                ('order', models.PositiveIntegerField(default=0)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='project.documents')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
