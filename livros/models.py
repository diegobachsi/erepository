from django.db import models
from django.contrib.auth.models import User

class LivrosManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )

class Livros(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    titulo = models.CharField('Título Livros', max_length=255)

    descricao = models.TextField('Descrição Simples', blank=True)

    url_imagem = models.CharField('Url da Imagem', max_length=255)

    atalho = models.SlugField('Atalho', null=False, unique=True)

    leu = models.BooleanField('Leu?', default=False)

    adicionado_em = models.DateTimeField('Adicionado em:', auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Livros'
        verbose_name_plural = 'Livros'
        ordering = ['adicionado_em']