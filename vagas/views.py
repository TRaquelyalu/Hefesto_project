from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from .forms import VagaForm, InscricaoForm
from .models import Vaga, Inscricao

# Página inicial dinâmica
def index(request):
    user_group = None
    if request.user.is_authenticated and request.user.groups.exists():
        user_group = request.user.groups.first().name
    return render(request, 'vagas/index.html', {'user_group': user_group})


# Login personalizado
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        tipo_usuario = request.POST.get('tipo_usuario')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if tipo_usuario == "candidato" and user.groups.filter(name="Candidato").exists():
                return redirect('painel_candidato')
            elif tipo_usuario == "empresa" and user.groups.filter(name="Empresa").exists():
                return redirect('painel_empresa')
            else:
                messages.error(request, "Tipo de usuário inválido.")
                return redirect('login')
        else:
            messages.error(request, "Credenciais inválidas.")
    return render(request, 'vagas/login.html')


# Painéis
@login_required
def painel_candidato(request):
    if not request.user.groups.filter(name="Candidato").exists():
        messages.error(request, "Acesso restrito a candidatos.")
        return redirect('index')
    return render(request, 'vagas/painel_candidato.html')


@login_required
def painel_empresa(request):
    if not request.user.groups.filter(name="Empresa").exists():
        messages.error(request, "Acesso restrito a empresas.")
        return redirect('index')
    return render(request, 'vagas/painel_empresa.html')


# Listar vagas
def listar_vagas(request):
    query = request.GET.get('q', '')
    vagas = Vaga.objects.filter(titulo__icontains=query) if query else Vaga.objects.all().order_by('-id')
    paginator = Paginator(vagas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vagas/listar_vagas.html', {
        'page_obj': page_obj,
        'query': query,
        'is_candidato': request.user.is_authenticated and request.user.groups.filter(name="Candidato").exists(),
        'is_empresa': request.user.is_authenticated and request.user.groups.filter(name="Empresa").exists(),
    })


# Gerenciamento de vagas (somente para empresas)
@login_required
def criar_vaga(request):
    if not request.user.groups.filter(name="Empresa").exists():
        messages.error(request, 'Apenas empresas podem criar vagas.')
        return redirect('index')
    form = VagaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        vaga = form.save(commit=False)
        vaga.criador = request.user
        vaga.save()
        messages.success(request, 'Vaga criada com sucesso!')
        return redirect('listar_vagas')
    return render(request, 'vagas/criar_vaga.html', {'form': form})


@login_required
def editar_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    if vaga.criador != request.user:
        messages.error(request, 'Você não tem permissão para editar esta vaga.')
        return redirect('listar_vagas')
    form = VagaForm(request.POST or None, instance=vaga)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Vaga atualizada com sucesso!')
        return redirect('listar_vagas')
    return render(request, 'vagas/editar_vaga.html', {'form': form})


@login_required
def excluir_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    if vaga.criador != request.user:
        messages.error(request, 'Você não tem permissão para excluir esta vaga.')
        return redirect('listar_vagas')
    vaga.delete()
    messages.success(request, 'Vaga excluída com sucesso!')
    return redirect('listar_vagas')


# Inscrições (somente para candidatos)
@login_required
def inscrever(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if not request.user.groups.filter(name="Candidato").exists():
        messages.error(request, 'Apenas candidatos podem se inscrever em vagas.')
        return redirect('listar_vagas')

    form = InscricaoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        inscricao = form.save(commit=False)
        inscricao.vaga = vaga
        inscricao.usuario = request.user
        inscricao.save()
        messages.success(request, 'Inscrição realizada com sucesso!')
        return redirect('listar_vagas')

    return render(request, 'vagas/inscrever.html', {'form': form, 'vaga': vaga})


@login_required
def listar_inscricoes(request):
    if not request.user.groups.filter(name="Candidato").exists():
        messages.error(request, 'Apenas candidatos podem visualizar inscrições.')
        return redirect('index')

    inscricoes = Inscricao.objects.filter(usuario=request.user)
    return render(request, 'vagas/listar_inscricoes.html', {'inscricoes': inscricoes})


@login_required
def excluir_inscricao(request, id):
    inscricao = get_object_or_404(Inscricao, id=id)
    if inscricao.usuario != request.user:
        messages.error(request, 'Você não tem permissão para excluir esta inscrição.')
        return redirect('listar_inscricoes')

    inscricao.delete()
    messages.success(request, 'Inscrição excluída com sucesso!')
    return redirect('listar_inscricoes')


# Registro de usuários
def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('index')
    return render(request, 'vagas/register.html', {'form': form})


# Logout customizado
def custom_logout(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('index')


# Páginas adicionais
def sobre_nos(request):
    return render(request, 'vagas/sobre_nos.html')


def contato(request):
    return render(request, 'vagas/contato.html')


def termos_de_uso(request):
    return render(request, 'vagas/termos_de_uso.html')














