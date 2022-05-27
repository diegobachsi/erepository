from django.contrib import admin

from .models import Livros

class LivrosAdmin(admin.ModelAdmin):

    list_display = ['titulo', 'atalho', 'leu', 'adicionado_em']
    search_fields = ['titulo', 'atalho']

admin.site.register(Livros, LivrosAdmin)
