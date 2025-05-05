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
    path('create/', views.create_news, name='create_news'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
