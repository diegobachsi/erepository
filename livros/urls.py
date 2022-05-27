from django import views
from django.urls import path

from . import views

app_name = 'livros'

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('editar/<int:id>', views.editar, name='editar'),
    path('deletar/<int:id>', views.deletar, name='deletar'),
    path('confirmar-delete/<int:id>', views.confirmar_delete, name='confirmar-delete'),
    path('lidos/', views.listar_lidos, name='lidos'),
    path('nao-lidos/', views.listar_not_lidos, name='nao-lidos'),
    path('detalhar/<int:id>', views.detalhar, name='detalhar'),
]
