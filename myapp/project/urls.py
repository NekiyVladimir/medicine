from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import EditProfileView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('employee_register/', views.employee_register, name='employee_register'),
    path('organization_register/', views.organization_register, name='organization_register'),
    path('documents/', views.documents, name='documents'),
    path('internal-docs/', views.internal_docs, name='internal_docs'),
    path('docs_detail//<int:doc_id>/', views.docs_detail, name='docs_detail'),
    path('internal-docs/add/', views.docs_add, name='docs_add'),
    path('create-document/', views.create_document, name='create_document'),
    # path('ckeditor/', include('ckeditor.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('news/', views.news, name='news'),
    path('new/<int:news_id>/', views.news_detail, name='news_detail'),
    path('create/', views.create_news, name='create_news'),
    path('tasks/', views.tasks, name='tasks'),
    path('my_tasks/', views.my_tasks, name='my_tasks'),
    path('task/<int:tasks_id>/', views.tasks_detail, name='tasks_detail'),
    path('create-tasks/', views.create_tasks, name='create_tasks'),
    path('tickets/', views.tickets, name='tickets'),
    path('my_tickets/', views.my_tickets, name='my_tickets'),
    path('tickets/<int:tickets_id>/', views.tickets_detail, name='tickets_detail'),
    path('create-tickets/', views.create_tickets, name='create_tickets'),
    path('add-comment-ticket/<int:tickets_id>/', views.add_comment_ticket, name='add_comment_ticket'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
