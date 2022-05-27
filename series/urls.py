from django import views
from django.urls import path

from . import views

app_name = 'series'

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('editar/<int:id>', views.editar, name='editar'),
    path('deletar/<int:id>', views.deletar, name='deletar'),
    path('confirmar-delete/<int:id>', views.confirmar_delete, name='confirmar-delete'),
    path('assistidos/', views.listar_assistidos, name='assistidos'),
    path('nao-assistidos/', views.listar_not_assistidos, name='nao-assistidos'),
    path('detalhar/<int:id>', views.detalhar, name='detalhar'),
]