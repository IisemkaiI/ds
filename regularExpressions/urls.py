from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # ваши view

urlpatterns = [
    # Главная страница — редактор regex
    path('', views.index, name='index'),

    # Регистрация
    path('register/', views.register, name='register'),

    # Вход
    path('login/', auth_views.LoginView.as_view(template_name='regularExpressions/login.html'), name='login'),

    # Выход
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]