from django.db import models
from django.contrib.auth.models import User


class EmployeePosition(models.Model):
    title = models.CharField(max_length=100, verbose_name='Должность', unique=True)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.title


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    position = models.ForeignKey('EmployeePosition', verbose_name='Должность', on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=15, verbose_name='телефон', blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='аватарка', blank=True, null=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.user.username


class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    name = models.CharField(max_length=100, verbose_name='Название организации')
    address = models.CharField(max_length=200, verbose_name='Адрес', blank=True, null=True)
    phone = models.CharField(max_length=15, verbose_name='телефон', blank=True, null=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class Documents(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название документа')  # Заголовок
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Дата создания
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')  # Дата обновления
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_model_authors',
                               verbose_name='ID пользователя, который создал')  # Автор
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_model_updaters',
                                   verbose_name='ID пользователя, который обновил')  # Обновлено кем
    version = models.DecimalField(max_digits=3, decimal_places=1, default=1.0, verbose_name='Версия документа')  # Версия

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.version += 0.1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст новости')
    image = models.ImageField(upload_to='news_files/', blank=True, null=True, verbose_name='Изображение')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата новости')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date']

    def __str__(self):
        return self.title


class Developer(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Разработчик'
        verbose_name_plural = 'Разработчики'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tasks(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    URGENCY_CHOICES = [
        ('low', 'Низкая'),
        ('medium', 'Средняя'),
        ('high', 'Высокая'),
    ]
    STATUS_CHOICES = [
        ('in_progress', 'В работе'),
        ('completed', 'Выполнена'),
        ('under_review', 'На рассмотрении'),
    ]
    title = models.CharField(max_length=255, verbose_name='Название задачи')
    description = models.TextField(verbose_name='Описание задачи')
    urgency = models.CharField(max_length=10, verbose_name='Срочность', choices=URGENCY_CHOICES)
    priority = models.CharField(max_length=10, verbose_name='Приоритет', choices=PRIORITY_CHOICES)
    customer = models.CharField(max_length=200, verbose_name='заказчик (организация)')
    assignee = models.ForeignKey(Developer, on_delete=models.CASCADE, verbose_name='исполнитель')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', default='1')
    file = models.FileField(upload_to='tasks_files/', blank=True, null=True, verbose_name='Файл')
    deadline = models.DateField(verbose_name='Дедлайн')
    status = models.CharField(max_length=15, verbose_name='Статус', choices=STATUS_CHOICES, default='under_review')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-title']

    def __str__(self):
        return self.title


class Tickets(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'В работе'),
        ('new', 'Новое'),
        ('decided', 'Решено'),
    ]
    title = models.CharField(max_length=255, verbose_name='Тема обращения')
    description = models.TextField(verbose_name='Описание обращения')
    customer = models.CharField(max_length=200, verbose_name='Заказчик (организация)')
    file = models.FileField(upload_to='tickets_files/', blank=True, null=True, verbose_name='Файл')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания обращения')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', default='1')
    status = models.CharField(max_length=15, verbose_name='Статус', choices=STATUS_CHOICES, default='new')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ['-title']

    def __str__(self):
        return self.title


class Document(models.Model):
    title = models.CharField(max_length=200)


class InternalDocs(models.Model):
    TYPE_CHOICES = [
        ('Приказ', 'Приказ'),
        ('Справка', 'Справка'),
        ('Заявление', 'Заявление'),
    ]
    title = models.CharField(max_length=200, verbose_name='Название документа')
    description = models.TextField(verbose_name='Описание документа')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания вн. док.')
    file = models.FileField(upload_to='docs_files/', blank=True, null=True, verbose_name='Файл')
    type = models.CharField(max_length=15, verbose_name='Тип документа', choices=TYPE_CHOICES)

    class Meta:
        verbose_name = 'Внутренний документ'
        verbose_name_plural = 'Внутренние документы'

    def __str__(self):
        return self.title


class Block(models.Model):
    BLOCK_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    document = models.ForeignKey(Document, related_name='blocks', on_delete=models.CASCADE)
    block_type = models.CharField(max_length=10, choices=BLOCK_TYPE_CHOICES)
    content = models.TextField(blank=True)  # Для текста или ссылки на видео
    image = models.ImageField(upload_to='images/', blank=True)  # Для изображений
    order = models.PositiveIntegerField(default=0)  # Для сортировки блоков

    class Meta:
        ordering = ['order']
