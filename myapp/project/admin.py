from django.contrib import admin
from .models import Documents, News


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author', 'version')  # Поля, которые будут отображаться в списке
    search_fields = ('title',)  # Поля, по которым можно будет искать


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author')  # Поля, которые будут отображаться в списке
    search_fields = ('title',)  # Поля, по которым можно будет искать


admin.site.register(Documents, DocumentsAdmin)
admin.site.register(News, NewsAdmin)
