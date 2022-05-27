from django.db import models
from django.contrib.auth.models import User

class SeriesManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )

class Series(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    titulo = models.CharField('Título Serie', max_length=255)

    descricao = models.TextField('Descrição Simples', blank=True)

    url_imagem = models.CharField('Url da Imagem', max_length=255)

    atalho = models.SlugField('Atalho', null=False, unique=True)

    assistiu = models.BooleanField('Assistiu?', default=False)

    adicionado_em = models.DateTimeField('Adicionado em:', auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = 'Series'
        ordering = ['adicionado_em']
