from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ProfileForm, UsuarioCreationForm, VagaForm
from .models import Vaga, Inscricao, Profile  # Certifique-se de incluir Profile aqui

# Página inicial
def index(request):
    vagas = Vaga.objects.all()
    return render(request, 'vagas/index.html', {'vagas': vagas})

# Registro de usuários
def register(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Criação automática de perfil
            Profile.objects.create(user=user)  # Certifique-se de que o modelo Profile está funcionando corretamente
            login(request, user)
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('index')
        else:
            messages.error(request, "Erro no cadastro. Verifique os dados.")
    else:
        form = UsuarioCreationForm()
    return render(request, 'vagas/register.html', {'form': form})

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
    return render(request, 'vagas/listar_vagas.html', {'vagas': vagas})

# Detalhes da vaga
def detalhes_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    return render(request, 'vagas/detalhes_vaga.html', {'vaga': vaga})

# Candidatar-se a uma vaga
@login_required
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    profile = getattr(request.user, 'profile', None)

    if not profile:
        messages.error(request, "Por favor, complete seu perfil antes de se candidatar.")
        return redirect('criar_perfil')

    Inscricao.objects.get_or_create(usuario=profile, vaga=vaga)
    messages.success(request, "Candidatura realizada com sucesso!")
    return HttpResponseRedirect(reverse('listar_vagas'))

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














