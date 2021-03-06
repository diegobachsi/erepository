# Generated by Django 3.2.6 on 2022-05-07 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filmes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, verbose_name='Título Filme')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição Simples')),
                ('url_imagem', models.CharField(max_length=255, verbose_name='Url da Imagem')),
                ('atalho', models.SlugField(unique=True, verbose_name='Atalho')),
                ('assistiu', models.BooleanField(default=False, verbose_name='Assistiu?')),
                ('adicionado_em', models.DateTimeField(auto_now_add=True, verbose_name='Adicionado em:')),
            ],
            options={
                'verbose_name': 'Filmes',
                'verbose_name_plural': 'Filmes',
                'ordering': ['adicionado_em'],
            },
        ),
    ]
