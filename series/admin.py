from django.contrib import admin

from .models import Series

class SeriesAdmin(admin.ModelAdmin):

    list_display = ['titulo', 'atalho', 'assistiu', 'adicionado_em']
    search_fields = ['titulo', 'atalho']

admin.site.register(Series, SeriesAdmin)