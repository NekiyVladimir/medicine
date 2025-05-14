from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import (Documents, News, Tasks, Developer, Tickets, EmployeePosition, Employee, Organization,
                     InternalDocs, Block)


class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'phone', 'avatar')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'address')


class BlockAdmin(admin.ModelAdmin):
    list_display = ('document', 'content', 'image', 'video')


class InternalDocsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'type')


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author', 'version')
    search_fields = ('title',)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author')
    search_fields = ('title',)


class TasksAdmin(admin.ModelAdmin):
    list_display = ('title', 'urgency', 'customer', 'assignee', 'deadline')
    search_fields = ('title',)


class TicketsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'customer', 'date', 'status')
    search_fields = ('title',)


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeePosition, EmployeePositionAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Documents, DocumentsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(Tickets, TicketsAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(InternalDocs, InternalDocsAdmin)
admin.site.register(Block, BlockAdmin)
