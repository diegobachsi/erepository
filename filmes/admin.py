from django.contrib import admin

from .models import Filmes

class FilmesAdmin(admin.ModelAdmin):

    list_display = ['id', 'titulo', 'atalho', 'assistiu', 'adicionado_em']
    search_fields = ['titulo', 'atalho']

admin.site.register(Filmes, FilmesAdmin)
