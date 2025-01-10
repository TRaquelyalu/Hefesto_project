from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ProfileForm, UsuarioCreationForm, VagaForm
from .models import Vaga, Inscricao, Profile, Usuario  # Substituído User por Usuario

# Página inicial
def index(request):
    vagas = Vaga.objects.all()
    return render(request, 'vagas/index.html', {'vagas': vagas})

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
            return redirect('index')
        else:
            messages.error(request, "Credenciais inválidas.")
    return render(request, 'vagas/login.html')

# Logout
def custom_logout(request):
    logout(request)
    messages.info(request, "Logout realizado com sucesso!")
    return redirect('index')

# Listar vagas
def listar_vagas(request):
    vagas = Vaga.objects.all()
    
    # Filtros
    tipo_de_vaga = request.GET.get('tipo_de_vaga')
    localizacao = request.GET.get('localizacao')
    status = request.GET.get('status')

    if tipo_de_vaga:
        vagas = vagas.filter(tipo_de_vaga=tipo_de_vaga)
    if localizacao:
        vagas = vagas.filter(localizacao__icontains=localizacao)
    if status:
        vagas = vagas.filter(status=status)

    return render(request, 'vagas/listar_vagas.html', {'vagas': vagas})

# Detalhes da vaga
def detalhes_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    return render(request, 'vagas/detalhes_vaga.html', {'vaga': vaga})

# Candidatar-se a uma vaga
def candidatar_vaga(request, vaga_id):
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar logado para se candidatar a uma vaga.")
        return redirect('login')

    # Obtenha a vaga e o perfil do usuário
    vaga = get_object_or_404(Vaga, id=vaga_id)
    profile = request.user.profile

    # Verifique se o usuário já se candidatou à vaga
    if Inscricao.objects.filter(usuario=profile, vaga=vaga).exists():
        messages.warning(request, "Você já se candidatou a esta vaga.")
    else:
        Inscricao.objects.create(usuario=profile, vaga=vaga)
        messages.success(request, "Candidatura realizada com sucesso!")

    return redirect('index')

# Criar perfil
@login_required
def criar_perfil(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Perfil criado com sucesso!")
            return redirect('listar_vagas')
        else:
            messages.error(request, "Erro ao criar perfil. Verifique os dados.")
    else:
        form = ProfileForm()
    return render(request, 'vagas/criar_perfil.html', {'form': form})

# Editar perfil
@login_required
def editar_perfil(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('listar_vagas')
        else:
            messages.error(request, "Erro ao atualizar perfil. Verifique os dados.")
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'vagas/editar_perfil.html', {'form': form})

@login_required
def criar_vaga(request):
    if request.method == "POST":
        form = VagaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaga criada com sucesso!")
            return redirect('listar_vagas')
    else:
        form = VagaForm()
    return render(request, 'vagas/criar_vaga.html', {'form': form})

# Páginas estáticas
def sobre_nos(request):
    return render(request, 'vagas/sobre_nos.html')

def contato(request):
    return render(request, 'vagas/contato.html')

def termos_de_uso(request):
    return render(request, 'vagas/termos_de_uso.html')

# Perfil do usuário
@login_required
def meu_perfil(request):
    profile = request.user.profile
    if request.method == "POST":
        profile.nome_completo = request.POST.get("nome_completo", "")
        profile.telefone = request.POST.get("telefone", "")
        profile.objetivo = request.POST.get("objetivo", "")
        profile.formacao = request.POST.get("formacao", "")
        profile.experiencia = request.POST.get("experiencia", "")
        profile.habilidades = request.POST.get("habilidades", "")
        profile.idiomas = request.POST.get("idiomas", "")
        profile.certificacoes = request.POST.get("certificacoes", "")
        profile.links = request.POST.get("links", "")
        profile.save()
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect('meu_perfil')
    return render(request, 'vagas/meu_perfil.html', {'user': request.user})

# Minhas candidaturas
@login_required
def minhas_candidaturas(request):
    inscricoes = Inscricao.objects.filter(usuario=request.user.profile)
    return render(request, 'vagas/minhas_candidaturas.html', {'inscricoes': inscricoes})











