from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import VagaForm, InscricaoForm, CustomUserCreationForm, CandidatoForm, EmpresaForm
from .models import Vaga, Inscricao, Profile

# Página inicial dinâmica
def index(request):
    user_group = None
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        user_group = request.user.profile.tipo_usuario
    return render(request, 'vagas/index.html', {'user_group': user_group})

# Cadastro de candidatos
def cadastro_candidato(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        profile_form = CandidatoForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.tipo_usuario = "Candidato"
            profile.save()
            messages.success(request, "Cadastro de candidato realizado com sucesso!")
            return redirect('login')
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = CustomUserCreationForm()
        profile_form = CandidatoForm()
    return render(request, 'vagas/cadastro_candidato.html', {'form': form, 'profile_form': profile_form})

# Cadastro de empresas
def cadastro_empresa(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        profile_form = EmpresaForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.tipo_usuario = "Empresa"
            profile.save()
            messages.success(request, "Cadastro de empresa realizado com sucesso!")
            return redirect('login')
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = CustomUserCreationForm()
        profile_form = EmpresaForm()
    return render(request, 'vagas/cadastro_empresa.html', {'form': form, 'profile_form': profile_form})

# Listar inscrições
@login_required
def listar_inscricoes(request):
    if request.user.profile.tipo_usuario != "Candidato":
        messages.error(request, "Acesso restrito a candidatos.")
        return redirect('index')
    inscricoes = Inscricao.objects.filter(usuario=request.user).select_related('vaga')
    return render(request, 'vagas/listar_inscricoes.html', {'inscricoes': inscricoes})

# Excluir inscrição
@login_required
def excluir_inscricao(request, id):
    inscricao = get_object_or_404(Inscricao, id=id)
    if inscricao.usuario != request.user:
        messages.error(request, "Você não tem permissão para excluir esta inscrição.")
        return redirect('listar_inscricoes')
    inscricao.delete()
    messages.success(request, "Inscrição excluída com sucesso!")
    return redirect('listar_inscricoes')

# Listar todas as vagas disponíveis
def listar_vagas(request):
    vagas = Vaga.objects.all()
    return render(request, 'vagas/listar_vagas.html', {'vagas': vagas})

@login_required
def criar_vaga(request):
    """Função para criar uma nova vaga (somente empresas)."""
    # Verifica se o usuário é uma empresa
    if request.user.profile.tipo_usuario != "Empresa":
        messages.error(request, "Apenas empresas podem criar vagas.")
        return redirect('index')

    # Processa o formulário de criação
    if request.method == "POST":
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user.username  # Associa a vaga à empresa logada
            vaga.save()
            messages.success(request, "Vaga criada com sucesso!")
            return redirect('painel_empresa')
    else:
        form = VagaForm()

    return render(request, 'vagas/criar_vaga.html', {'form': form})

@login_required
def editar_vaga(request, id):
    """Função para editar uma vaga existente."""
    vaga = get_object_or_404(Vaga, id=id)

    # Verifica se a vaga pertence à empresa logada
    if vaga.empresa != request.user.username:
        messages.error(request, "Você não tem permissão para editar esta vaga.")
        return redirect('painel_empresa')

    if request.method == "POST":
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaga atualizada com sucesso!")
            return redirect('painel_empresa')
    else:
        form = VagaForm(instance=vaga)

    return render(request, 'vagas/editar_vaga.html', {'form': form, 'vaga': vaga})

@login_required
def excluir_vaga(request, id):
    """Função para excluir uma vaga."""
    vaga = get_object_or_404(Vaga, id=id)

    # Verifica se a vaga pertence à empresa logada
    if vaga.empresa != request.user.username:
        messages.error(request, "Você não tem permissão para excluir esta vaga.")
        return redirect('painel_empresa')

    vaga.delete()
    messages.success(request, "Vaga excluída com sucesso!")
    return redirect('painel_empresa')

def detalhes_vaga(request, id):
    """Exibe os detalhes de uma vaga específica."""
    vaga = get_object_or_404(Vaga, id=id)
    return render(request, 'vagas/detalhes_vaga.html', {'vaga': vaga})

@login_required
def inscrever(request, vaga_id):
    """Permite que candidatos se inscrevam em uma vaga."""
    vaga = get_object_or_404(Vaga, id=vaga_id)

    # Verifica se o usuário é um candidato
    if request.user.profile.tipo_usuario != "Candidato":
        messages.error(request, "Apenas candidatos podem se inscrever em vagas.")
        return redirect('listar_vagas')

    # Processa o formulário de inscrição
    if request.method == "POST":
        form = InscricaoForm(request.POST)
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.vaga = vaga
            inscricao.usuario = request.user
            inscricao.save()
            messages.success(request, "Inscrição realizada com sucesso!")
            return redirect('painel_candidato')
        else:
            messages.error(request, "Houve um problema com sua inscrição. Tente novamente.")
    else:
        form = InscricaoForm()

    return render(request, 'vagas/inscrever.html', {'form': form, 'vaga': vaga})

def login_view(request):
    """Exibe a página de login e autentica o usuário."""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redireciona o usuário com base no tipo de perfil
            if hasattr(user, 'profile'):
                if user.profile.tipo_usuario == "Candidato":
                    return redirect('painel_candidato')
                elif user.profile.tipo_usuario == "Empresa":
                    return redirect('painel_empresa')
            return redirect('index')
        else:
            messages.error(request, "Credenciais inválidas. Tente novamente.")
    return render(request, 'vagas/login.html')

def custom_logout(request):
    """Realiza o logout do usuário."""
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect('index')

@login_required
def painel_candidato(request):
    """Exibe o painel para candidatos."""
    # Verifica se o usuário logado é um candidato
    if request.user.profile.tipo_usuario != "Candidato":
        messages.error(request, "Acesso restrito a candidatos.")
        return redirect('index')

    # Busca inscrições associadas ao candidato logado
    inscricoes = Inscricao.objects.filter(usuario=request.user).select_related('vaga')

    # Renderiza o painel do candidato
    return render(request, 'vagas/painel_candidato.html', {'inscricoes': inscricoes})

@login_required
def painel_empresa(request):
    """Exibe o painel para empresas."""
    # Verifica se o usuário logado é uma empresa
    if request.user.profile.tipo_usuario != "Empresa":
        messages.error(request, "Acesso restrito a empresas.")
        return redirect('index')

    # Busca vagas criadas pela empresa logada
    vagas = Vaga.objects.filter(empresa=request.user.username)

    # Renderiza o painel da empresa
    return render(request, 'vagas/painel_empresa.html', {'vagas': vagas})

def sobre_nos(request):
    """Renderiza a página 'Sobre Nós'."""
    return render(request, 'vagas/sobre_nos.html')

def contato(request):
    """Renderiza a página 'Contato'."""
    return render(request, 'vagas/contato.html')

def termos_de_uso(request):
    """Renderiza a página de Termos de Uso."""
    return render(request, 'vagas/termos_de_uso.html')

def index_visitantes(request):
    """Renderiza a página inicial para visitantes, listando as vagas publicadas."""
    vagas = Vaga.objects.all().order_by('-data_publicacao')
    return render(request, 'vagas/index_visitantes.html', {'vagas': vagas})













