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

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.version += 0.1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

