from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from .models import Series

from .forms import FormCadastrar

@login_required(login_url='contas:login')
def index(request):

    series = Series.objects.filter(user=request.user)

    template = 'series.html'
    context = {
        'series': series
    }

    return render(request, template, context)

@login_required(login_url='contas:login')
def cadastrar(request):

    context = {}

    if request.method == 'POST':
        form = FormCadastrar(request.POST)

        #verifica se o preenchimento do form foi válido
        if form.is_valid():
            context['is_valid'] = True
        
            #recebe os valores digitamos correspondente a cada campo do form
            titulo = request.POST['titulo']
            descricao = request.POST['descricao'] 
            url_imagem = request.POST['url_imagem']
            assistiu = request.POST.get('assistiu', False)

            #converte o valor do checkbox esta_em_cartaz para salvar no bd
            if assistiu == 'on':
                assistiu = True
            else:
                assistiu = False

            #converte o título para slug (formato atalho)
            atalho = slugify(titulo+'-'+str(request.user))

            try:
                #cadastra o filme
                cadastra_serie = Series(user=request.user, titulo=titulo, descricao=descricao, url_imagem=url_imagem,
                                    assistiu=assistiu, atalho=atalho)
                cadastra_serie.save()
                context['foiCadastrado'] = True
            except:
                context['foiCadastrado'] = False

            series = Series.objects.filter(user=request.user)

            context['series'] = series
            context['serie'] = titulo

            return render(request, 'series.html', context)

    else:
        form = FormCadastrar()

    context['form'] = form

    return render(request, 'cadastrar_serie.html', context)

@login_required(login_url='contas:login')
def editar(request, id):

    serie = get_object_or_404(Series,id=id)

    context = {}

    if request.method == 'POST':
        form = FormCadastrar(request.POST)

        #verifica se o preenchimento do form foi válido
        if form.is_valid():
            context['is_valid'] = True
        
            #recebe os valores digitamos correspondente a cada campo do form
            titulo = request.POST['titulo']
            descricao = request.POST['descricao'] 
            url_imagem = request.POST['url_imagem']
            assistiu = request.POST.get('assistiu', False)

            #converte o valor do checkbox esta_em_cartaz para salvar no bd
            if assistiu == 'on':
                assistiu = True
            else:
                assistiu = False

            #converte o título para slug (formato atalho)
            atalho = slugify(titulo+'-'+str(request.user))

            try:
                #edita o filme
                serie_a_editar = Series.objects.filter(id=id)
                serie_a_editar.update(titulo=titulo, descricao=descricao, url_imagem=url_imagem,
                                    assistiu=assistiu, atalho=atalho)
                context['foiEditado'] = True
            except:
                context['foiEditado'] = False

            series = Series.objects.filter(user=request.user)

            context['series'] = series
            context['serie'] = titulo

            return render(request, 'series.html', context)
    else:
        form = FormCadastrar()

        form.initial['titulo'] = serie.titulo
        form.initial['descricao'] = serie.descricao
        form.initial['url_imagem'] = serie.url_imagem
        form.initial['assistiu'] = serie.assistiu

    context['form'] = form
    context['id'] = id

    return render(request, 'editar_serie.html', context)

@login_required(login_url='contas:login')
def confirmar_delete(request, id):

    titulo = Series.objects.filter(id=id).values('titulo')[0]['titulo']

    context = {
        'titulo': titulo,
        'id': id
    }

    return render(request, 'confirmar_delete_serie.html', context)

@login_required(login_url='contas:login')
def deletar(request, id):

    serie = get_object_or_404(Series,id=id) 
    serie.delete()

    series = Series.objects.filter(user=request.user)

    context = {
        'foiDeletado': True,
        'series': series,
        'serie': serie
    }

    return render(request, 'series.html', context)

@login_required(login_url='contas:login')
def listar_assistidos(request):

    assistidos = Series.objects.filter(user=request.user, assistiu=True)

    context = {
        'series': assistidos
    }

    return render(request, 'series.html', context)

@login_required(login_url='contas:login')
def listar_not_assistidos(request):

    not_assistidos = Series.objects.filter(user=request.user, assistiu=False)

    context = {
        'series': not_assistidos
    }

    return render(request, 'series.html', context)

@login_required(login_url='contas:login')
def detalhar(request, id):

    serie = get_object_or_404(Series,id=id) 

    context = {
        'serie': serie
    }

    return render(request, 'detalhar_serie.html', context)