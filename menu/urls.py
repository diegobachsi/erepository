from django import views
from django.urls import path

from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('exportar_json/', views.exportar_json, name='exportar_json'),
    path('importar_dados_filmes_series/', views.importar_dados_filmes_series, name='importar_dados_filmes_series'),
    path('importar_dados_livros/', views.importar_dados_livros, name='importar_dados_livros'),
    path('cadastrar_via_import/', views.guardar_dados_bd, name='cadastrar_via_import')
]

