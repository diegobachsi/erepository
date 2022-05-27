# Generated by Django 3.2.6 on 2022-05-08 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Livros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, verbose_name='Título Livros')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição Simples')),
                ('url_imagem', models.CharField(max_length=255, verbose_name='Url da Imagem')),
                ('atalho', models.SlugField(unique=True, verbose_name='Atalho')),
                ('leu', models.BooleanField(default=False, verbose_name='Leu?')),
                ('adicionado_em', models.DateTimeField(auto_now_add=True, verbose_name='Adicionado em:')),
            ],
            options={
                'verbose_name': 'Livros',
                'verbose_name_plural': 'Livros',
                'ordering': ['adicionado_em'],
            },
        ),
    ]
