from django import views
from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'contas'

urlpatterns = [
    path('', views.logar, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('validate/<username>/', views.registerValidate, name='validate'),
]
