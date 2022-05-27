from django.db import models
from django.contrib.auth.models import User

class FilmesManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )

class Filmes(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    titulo = models.CharField('Título Filme', max_length=255)

    descricao = models.TextField('Descrição Simples', blank=True)

    url_imagem = models.CharField('Url da Imagem', max_length=255)

    atalho = models.SlugField('Atalho', null=False, unique=True)

    assistiu = models.BooleanField('Assistiu?', default=False)

    adicionado_em = models.DateTimeField('Adicionado em:', auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Filmes'
        verbose_name_plural = 'Filmes'
        ordering = ['adicionado_em']