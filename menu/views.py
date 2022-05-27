from re import T
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from filmes.models import Filmes
from series.models import Series
from livros.models import Livros
from .forms import FormImportarFilmes
from shutil import make_archive
from django.core import serializers
import requests
import json
from django.template.defaultfilters import slugify

@login_required(login_url='contas:login')
def index(request):

    count_filmes = Filmes.objects.filter(user=request.user).count()
    count_series = Series.objects.filter(user=request.user).count()
    count_livros = Livros.objects.filter(user=request.user).count()

    count_filmes_assistidos = Filmes.objects.filter(user=request.user, assistiu=True).count()
    count_series_assistidas = Series.objects.filter(user=request.user, assistiu=True).count()
    count_livros_lidos = Livros.objects.filter(user=request.user, leu=True).count()

    try:
        progresso_filmes = (count_filmes_assistidos / count_filmes) * 100
    except:
        progresso_filmes = 0

    try:
        progresso_series = (count_series_assistidas / count_series) * 100
    except:
        progresso_series = 0

    try:
        progresso_livros = (count_livros_lidos / count_livros) * 100
    except:
        progresso_livros = 0

    template = 'menu.html'
    context = {
        'count_filmes': count_filmes,
        'count_series': count_series,
        'count_livros': count_livros,
        'count_filmes_assistidos': count_filmes_assistidos,
        'count_series_assistidas': count_series_assistidas,
        'count_livros_lidos': count_livros_lidos,
        'progresso_filmes': progresso_filmes,
        'progresso_series': progresso_series,
        'progresso_livros': progresso_livros
    }

    return render(request, template, context)

@login_required(login_url='contas:login')
def sobre(request):

    template = 'sobre.html'
    context = {}

    return render(request, template, context)

@login_required(login_url='contas:login')
def exportar_json(request):

    template = 'json.html'

    dados_filmes = serializers.serialize("json", Filmes.objects.filter(user=request.user))
    dados_series = serializers.serialize("json", Series.objects.filter(user=request.user))
    dados_livros = serializers.serialize("json", Livros.objects.filter(user=request.user))

    #filmes
    f = open('static/json/dados_filmes.json', 'w')
    json.dump(dados_filmes, f, sort_keys=True, indent=4)

    #series
    f = open('static/json/dados_series.json', 'w')
    json.dump(dados_series, f, sort_keys=True, indent=4)

    #livros
    f = open('static/json/dados_livros.json', 'w')
    json.dump(dados_livros, f, sort_keys=True, indent=4)

    f.close()

    make_archive('static/json/', 'zip', 'static/json/')

    return render(request, template)

@login_required(login_url='contas:login')
def importar_dados_livros(request):
    context = {}

    if request.method == 'POST':
        form = FormImportarFilmes(request.POST)

        #verifica se o preenchimento do form foi válido
        if form.is_valid():

            context['is_valid'] = True

            titulo = request.POST['titulo']

            try:

                req = requests.get(f'https://api.mercadoeditorial.org/api/v1.2/book?titulo={titulo}')
                content = json.loads(req.text)
          

                content = content.get('books')[0]

                titulo = content.get('titulo')

                url_imagem = content.get('imagens').get('imagem_primeira_capa').get('pequena')

                #sinopse = content.get('sinopse')

                context['tipo'] = 'livros'
                context['titulo'] = titulo
                context['url_imagem'] = url_imagem

                context['existe'] = True
                   
            except:
                pass

    else:
        form = FormImportarFilmes()

    context['form'] = form

    return render(request, 'importar_dados_livros.html', context)

@login_required(login_url='contas:login')
def importar_dados_filmes_series(request):

    context = {}

    if request.method == 'POST':
        form = FormImportarFilmes(request.POST)

        #verifica se o preenchimento do form foi válido
        if form.is_valid():

            context['is_valid'] = True

            titulo = request.POST['titulo']

            try:
                req = requests.get(f'http://www.omdbapi.com/?t={titulo}&apikey=7bb6880e')
                content = json.loads(req.text)
                context['titulo'] = content['Title']
                context['url_imagem'] = content['Poster']
                context['tipo'] = content['Type']

                if content['Response']:
                    context['existe'] = True
                else:
                    context['existe'] = False
            except:
                pass
            
    else:
        form = FormImportarFilmes()

    context['form'] = form

    return render(request, 'importar_dados_filmes_series.html', context)

@login_required(login_url='contas:login')
def guardar_dados_bd(request):

    context = {}

    titulo = request.GET.get('titulo')
    tipo = request.GET.get('tipo')
   

    if tipo == 'movie' or tipo == 'series':

        req = requests.get(f'http://www.omdbapi.com/?t={titulo}&apikey=7bb6880e' )
        content = json.loads(req.text)

        if tipo == 'movie':

            #realiza consulta no bd para ver se o filme já existe
            filme_existe = Filmes.objects.filter(user=request.user, titulo=titulo)

            context['tipo'] = 'Filme'

            if not filme_existe: 
                cadastra_filme = Filmes(user=request.user, titulo=titulo, descricao=content['Plot'], url_imagem=content['Poster'],
                                        assistiu=False, atalho=slugify(titulo+'-'+str(request.user)))
                cadastra_filme.save()

                context['gravado'] = True
                
            else:
                context['gravado'] = False

        else:

            #realiza consulta no bd para ver se o filme já existe
            serie_existe = Series.objects.filter(user=request.user, titulo=titulo)

            context['tipo'] = 'Série'

            if not serie_existe: 
                cadastra_serie = Series(user=request.user, titulo=titulo, descricao=content['Plot'], url_imagem=content['Poster'],
                                        assistiu=False, atalho=slugify(titulo+'-'+str(request.user)))
                cadastra_serie.save()

                context['gravado'] = True
                
            else:
                context['gravado'] = False

        return render(request, 'importar_dados_filmes_series.html', context)

    else:

        req = requests.get('https://api.mercadoeditorial.org/api/v1.2/book?titulo=' + titulo)
        content = json.loads(req.text)

        content = content.get('books')[0]
        url_imagem = content.get('imagens').get('imagem_primeira_capa').get('pequena')
        sinopse = content.get('sinopse')

        #realiza consulta no bd para ver se o filme já existe
        livro_existe = Livros.objects.filter(user=request.user, titulo=titulo)

        context['tipo'] = 'Livro'

        if not livro_existe: 
            cadastra_livro = Livros(user=request.user, titulo=titulo, descricao=sinopse, url_imagem=url_imagem,
                                    leu=False, atalho=slugify(titulo+'-'+str(request.user)))
            cadastra_livro.save()

            context['gravado'] = True
        else:
            context['gravado'] = False

        return render(request, 'importar_dados_livros.html', context)

    