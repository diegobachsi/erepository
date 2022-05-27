from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from .models import Filmes
from .forms import FormCadastrar

@login_required(login_url='contas:login')
def index(request):

    template = 'filmes.html'

    filmes = Filmes.objects.filter(user=request.user)

    context = {
        'filmes': filmes
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
                cadastra_filme = Filmes(user=request.user, titulo=titulo, descricao=descricao, url_imagem=url_imagem,
                                    assistiu=assistiu, atalho=atalho)
                cadastra_filme.save()
                context['foiCadastrado'] = True
            except:
                context['foiCadastrado'] = False

            filmes = Filmes.objects.filter(user=request.user)

            context['filmes'] = filmes
            context['filme'] = titulo

            return render(request, 'filmes.html', context)

    else:
        form = FormCadastrar()

    context['form'] = form

    return render(request, 'cadastrar_filme.html', context)

@login_required(login_url='contas:login')
def editar(request, id):

    filme = get_object_or_404(Filmes,id=id)

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
                filme_a_editar = Filmes.objects.filter(id=id)
                filme_a_editar.update(titulo=titulo, descricao=descricao, url_imagem=url_imagem,
                                    assistiu=assistiu, atalho=atalho)
                context['foiEditado'] = True
            except:
                context['foiEditado'] = False

            filmes = Filmes.objects.filter(user=request.user)

            context['filmes'] = filmes
            context['filme'] = titulo

            return render(request, 'filmes.html', context)
    else:
        form = FormCadastrar()

        #aparecer os campos preenchidos
        form.initial['titulo'] = filme.titulo
        form.initial['descricao'] = filme.descricao
        form.initial['url_imagem'] = filme.url_imagem
        form.initial['assistiu'] = filme.assistiu

    context['form'] = form
    context['id'] = id

    return render(request, 'editar_filme.html', context)

@login_required(login_url='contas:login')
def confirmar_delete(request, id):

    titulo = Filmes.objects.filter(id=id).values('titulo')[0]['titulo']

    context = {
        'titulo': titulo,
        'id': id
    }

    return render(request, 'confirmar_delete.html', context)

@login_required(login_url='contas:login')
def deletar(request, id):

    filme = get_object_or_404(Filmes,id=id) 
    filme.delete()

    filmes = Filmes.objects.filter(user=request.user)

    context = {
        'foiDeletado': True,
        'filmes': filmes,
        'filme': filme
    }

    return render(request, 'filmes.html', context)

@login_required(login_url='contas:login')
def listar_assistidos(request):

    assistidos = Filmes.objects.filter(user=request.user, assistiu=True)

    context = {
        'filmes': assistidos
    }

    return render(request, 'filmes.html', context)

@login_required(login_url='contas:login')
def listar_not_assistidos(request):

    not_assistidos = Filmes.objects.filter(user=request.user, assistiu=False)

    context = {
        'filmes': not_assistidos
    }

    return render(request, 'filmes.html', context)

@login_required(login_url='contas:login')
def detalhar(request, id):

    filme = get_object_or_404(Filmes,id=id) 

    context = {
        'filme': filme
    }

    return render(request, 'detalhar_filme.html', context)