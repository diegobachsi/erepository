from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from .forms import FormCadastrar

from .models import Livros

@login_required(login_url='contas:login')
def index(request):

    template = 'livros.html'

    livros = Livros.objects.filter(user=request.user)

    context = {
        'livros': livros
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
            leu = request.POST.get('leu', False)

            #converte o valor do checkbox esta_em_cartaz para salvar no bd
            if leu == 'on':
                leu = True
            else:
                leu = False

            #converte o título para slug (formato atalho)
            atalho = slugify(titulo+'-'+str(request.user))

            try:
                #cadastra o livro
                cadastra_filme = Livros(user=request.user, titulo=titulo, descricao=descricao, url_imagem=url_imagem,
                                    leu=leu, atalho=atalho)
                cadastra_filme.save()
                context['foiCadastrado'] = True
            except:
                context['foiCadastrado'] = False

            livros = Livros.objects.filter(user=request.user)

            context['livros'] = livros
            context['livro'] = titulo

            return render(request, 'livros.html', context)

    else:
        form = FormCadastrar()

    context['form'] = form

    return render(request, 'cadastrar_livro.html', context)

@login_required(login_url='contas:login')
def editar(request, id):

    filme = get_object_or_404(Livros,id=id)

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
            leu = request.POST.get('leu', False)

            #converte o valor do checkbox esta_em_cartaz para salvar no bd
            if leu == 'on':
                leu = True
            else:
                leu = False

            #converte o título para slug (formato atalho)
            atalho = slugify(titulo+'-'+str(request.user))

            try:
                #cadastra o livro
                filme_a_editar = Livros.objects.filter(id=id)
                filme_a_editar.update(titulo=titulo, descricao=descricao, url_imagem=url_imagem,
                                    leu=leu, atalho=atalho)
                context['foiEditado'] = True
            except:
                context['foiEditado'] = False

            livros = Livros.objects.filter(user=request.user)

            context['livros'] = livros
            context['livro'] = titulo

            return render(request, 'livros.html', context)
    else:
        form = FormCadastrar()

        form.initial['titulo'] = filme.titulo
        form.initial['descricao'] = filme.descricao
        form.initial['url_imagem'] = filme.url_imagem
        form.initial['leu'] = filme.leu

    context['form'] = form
    context['id'] = id

    return render(request, 'editar_livro.html', context)

@login_required(login_url='contas:login')
def confirmar_delete(request, id):

    titulo = Livros.objects.filter(id=id).values('titulo')[0]['titulo']

    context = {
        'titulo': titulo,
        'id': id
    }

    return render(request, 'confirmar_delete_livro.html', context)

@login_required(login_url='contas:login')
def deletar(request, id):

    context = {}

    livro = get_object_or_404(Livros,id=id) 
    livro.delete()

    livros = Livros.objects.filter(user=request.user)

    context = {
        'foiDeletado': True,
        'livros': livros,
        'livro': livro
    }

    return render(request, 'livros.html', context)

@login_required(login_url='contas:login')
def listar_lidos(request):

    lidos = Livros.objects.filter(user=request.user, leu=True)

    context = {
        'livros': lidos
    }

    return render(request, 'livros.html', context)

@login_required(login_url='contas:login')
def listar_not_lidos(request):

    not_lidos = Livros.objects.filter(user=request.user, leu=False)

    context = {
        'livros': not_lidos
    }

    return render(request, 'livros.html', context)

@login_required(login_url='contas:login')
def detalhar(request, id):

    livro = get_object_or_404(Livros,id=id) 

    context = {
        'livro': livro
    }

    return render(request, 'detalhar_livro.html', context)