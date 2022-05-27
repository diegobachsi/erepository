from django.contrib import admin
from django.urls import path, include
from contas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
    path('login/', include('contas.urls')),
    path('filmes/', include('filmes.urls')),
    path('series/', include('series.urls')),
    path('livros/', include('livros.urls')),
    path('reset/<uidb64>/<token>/', views.PasswordConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(template_name='partials/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(template_name='partials/password_reset_complete.html'), name='password_reset_complete'),
]
