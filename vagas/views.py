from itertools import count
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q  # Import necessário para filtros de busca
from .forms import ProfileForm, UsuarioCreationForm, VagaForm
from .models import Vaga, Candidatura, Profile, Usuario
from .forms import VagaForm
from .models import Vaga, Candidatura


# Página inicial: exibe todas as vagas disponíveis
def index(request):
    vagas = Vaga.objects.all()
    return render(request, 'vagas/index.html', {'vagas': vagas})


# Listar vagas disponíveis
def listar_vagas(request):
    # Captura os filtros enviados pelo usuário
    query = request.GET.get('q', '').strip()  # Busca por título ou descrição
    localizacao = request.GET.get('localizacao', '').strip()  # Filtro por localização
    tipo = request.GET.get('tipo', '').strip()  # Filtro por tipo

    # Busca todas as vagas inicialmente
    vagas = Vaga.objects.all()

    # Aplicar filtros se os campos estiverem preenchidos
    if query:
        vagas = vagas.filter(Q(titulo__icontains=query) | Q(descricao__icontains=query))
    if localizacao:
        vagas = vagas.filter(localizacao__icontains=localizacao)
    if tipo:
        vagas = vagas.filter(tipo__icontains=tipo)

    # Renderiza a página de listagem de vagas com os filtros aplicados
    
    return render(request, 'vagas/listar_vagas.html', {'vagas': vagas})
# Registro de usuários
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        full_name = request.POST.get("full_name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return redirect("register")

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já está em uso.")
            return redirect("register")

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Email já está em uso.")
            return redirect("register")

        try:
            user = Usuario.objects.create_user(username=username, email=email, password=password)
            user.first_name = full_name
            user.save()
            messages.success(request, "Conta criada com sucesso!")
            return redirect("login")
        except IntegrityError:
            messages.error(request, "Erro ao criar a conta. Tente novamente.")
            return redirect("register")

    return render(request, "vagas/register.html")


# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect(request.GET.get('next', 'index'))  # Redireciona para a página anterior
        else:
            messages.error(request, "Credenciais inválidas.")
    return render(request, 'vagas/login.html')


# Logout
def custom_logout(request):
    logout(request)
    messages.info(request, "Logout realizado com sucesso!")
    return redirect('index')


# Detalhes da vaga
def detalhes_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    return render(request, 'vagas/detalhes_vaga.html', {'vaga': vaga})


# Candidatar-se a uma vaga
@login_required
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    candidato = request.user

    # Verificar se o usuário já se candidatou
    if Candidatura.objects.filter(vaga=vaga, candidato=candidato).exists():
        messages.error(request, "Você já se candidatou a esta vaga.")
        return redirect('detalhes_vaga', vaga_id=vaga_id)

    # Criar a candidatura
    try:
        Candidatura.objects.create(vaga=vaga, candidato=candidato)
        messages.success(request, "Candidatura realizada com sucesso!")
    except Exception as e:
        messages.error(request, f"Erro ao realizar candidatura: {e}")

    return redirect('detalhes_vaga', vaga_id=vaga_id)


# Perfil do usuário
@login_required
def meu_perfil(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('meu_perfil')
        else:
            messages.error(request, "Erro ao atualizar o perfil.")
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'vagas/meu_perfil.html', {'form': form})


# Minhas candidaturas
@login_required
def minhas_candidaturas(request):
    candidaturas = Candidatura.objects.filter(candidato=request.user).select_related('vaga')
    return render(request, 'vagas/minhas_candidaturas.html', {'candidaturas': candidaturas})


# Criar vaga
@login_required
def criar_vaga(request):
    """
    View para criação de vagas.
    Apenas usuários autenticados podem criar uma vaga.
    """
    if request.method == "POST":
        form = VagaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaga criada com sucesso!")
            return redirect('listar_vagas')
        else:
            messages.error(request, "Erro ao salvar a vaga. Verifique os dados.")
    else:
        form = VagaForm()

    return render(request, 'vagas/criar_vaga.html', {'form': form})

# Listar candidatos por vaga
@login_required
def listar_candidatos_por_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    candidaturas = Candidatura.objects.filter(vaga=vaga).select_related('candidato')
    return render(request, 'vagas/listar_candidatos_por_vaga.html', {'vaga': vaga, 'candidaturas': candidaturas})

@login_required
def criar_perfil(request):
    """
    View para criação do perfil do usuário.
    """
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Perfil criado com sucesso!")
            return redirect('meu_perfil')
        else:
            messages.error(request, "Erro ao criar perfil. Verifique os dados.")
    else:
        form = ProfileForm()

    return render(request, 'vagas/criar_perfil.html', {'form': form})

@login_required
def editar_perfil(request):
    """
    View para edição do perfil do usuário.
    Apenas usuários autenticados podem acessar.
    """
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('meu_perfil')
        else:
            messages.error(request, "Erro ao atualizar o perfil. Verifique os dados.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'vagas/editar_perfil.html', {'form': form})

def sobre_nos(request):
    """
    View para a página "Sobre Nós".
    Exibe informações sobre a plataforma.
    """
    return render(request, 'vagas/sobre_nos.html')

def contato(request):
    """
    View para a página de contato.
    Exibe informações de contato da plataforma.
    """
    return render(request, 'vagas/contato.html')

def termos_de_uso(request):
    """
    View para a página de termos de uso.
    Exibe os termos e condições da plataforma.
    """
    return render(request, 'vagas/termos_de_uso.html')

@login_required
def listar_candidaturas(request):
    query = request.GET.get('q')  # Filtro por título da vaga
    candidaturas = Candidatura.objects.select_related('vaga', 'candidato')

    if query:
        candidaturas = candidaturas.filter(vaga__titulo__icontains=query)

    candidaturas_por_vaga = (
        candidaturas.values('vaga__titulo', 'vaga__id')
        .annotate(total=count('id'))
        .order_by('vaga__titulo')
    )

    return render(request, 'vagas/listar_candidaturas.html', {
        'candidaturas': candidaturas,
        'candidaturas_por_vaga': candidaturas_por_vaga,
    })

def relatorio_candidaturas(request):
    vagas = Vaga.objects.prefetch_related('candidatura_set')  # Carrega vagas e candidaturas associadas
    return render(request, 'vagas/relatorio_candidaturas.html', {'vagas': vagas})