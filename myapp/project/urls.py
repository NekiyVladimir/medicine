from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('documents/', views.documents, name='documents'),
    path('create-document/', views.create_document, name='create_document'),
    # path('ckeditor/', include('ckeditor.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('profile/', views.profile, name='profile'),
    path('news/', views.news, name='news'),
    path('new/<int:news_id>/', views.news_detail, name='news_detail'),
    path('create/', views.create_news, name='create_news'),
    path('tasks/', views.tasks, name='tasks'),
    path('task/<int:tasks_id>/', views.tasks_detail, name='tasks_detail'),
    path('create-tasks/', views.create_tasks, name='create_tasks'),
    path('tickets/', views.tickets, name='tickets'),
    path('tickets/<int:tickets_id>/', views.tickets_detail, name='tickets_detail'),
    path('create-tickets/', views.create_tickets, name='create_tickets'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
