from django.db import models
from django.contrib.auth.models import User


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
    file = models.FileField(upload_to='news_files/', blank=True, null=True, verbose_name='Файл')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата новости')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date']

    def __str__(self):
        return self.title


class Document(models.Model):
    title = models.CharField(max_length=200)


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
