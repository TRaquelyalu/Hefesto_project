from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import VagaForm, InscricaoForm, ProfileForm
from .models import Vaga, Inscricao

# Página inicial
def index(request):
    vagas = Vaga.objects.all()
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile.tipo_usuario == 'Candidato':
            inscricoes = Inscricao.objects.filter(usuario=request.user.username)
            return render(request, 'vagas/index_candidato.html', {
                'vagas': vagas,
                'inscricoes': inscricoes
            })
        elif hasattr(request.user, 'profile') and request.user.profile.tipo_usuario == 'Recrutador':
            return redirect('tela_inicial_recrutador')
    return render(request, 'vagas/index.html', {'vagas': vagas})

# Listar vagas
def listar_vagas(request):
    query = request.GET.get('q')
    vagas = Vaga.objects.filter(titulo__icontains=query) if query else Vaga.objects.all()
    paginator = Paginator(vagas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'vagas/listar_vagas.html', {'page_obj': page_obj, 'query': query})

# Criar vaga
@login_required
def criar_vaga(request):
    if not hasattr(request.user, 'profile') or request.user.profile.tipo_usuario != 'Recrutador':
        messages.error(request, 'Apenas recrutadores podem criar vagas.')
        return redirect('index')
    form = VagaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        vaga = form.save(commit=False)
        vaga.save()
        messages.success(request, 'Vaga criada com sucesso!')
        return redirect('listar_vagas')
    return render(request, 'vagas/criar_vaga.html', {'form': form})

# Editar vaga
@login_required
def editar_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    form = VagaForm(request.POST or None, instance=vaga)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Vaga atualizada com sucesso!')
        return redirect('listar_vagas')
    return render(request, 'vagas/editar_vaga.html', {'form': form})

# Excluir vaga
@login_required
def excluir_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    vaga.delete()
    messages.success(request, 'Vaga excluída com sucesso!')
    return redirect('listar_vagas')

# Inscrever-se em uma vaga
@login_required
def inscrever(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    form = InscricaoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        inscricao = form.save(commit=False)
        inscricao.vaga = vaga
        inscricao.usuario = request.user.username
        inscricao.save()
        messages.success(request, 'Inscrição realizada com sucesso!')
        return redirect('listar_vagas')
    return render(request, 'vagas/inscrever.html', {'form': form, 'vaga': vaga})

# Listar inscrições
@login_required
def listar_inscricoes(request):
    inscricoes = Inscricao.objects.select_related('vaga').filter(usuario=request.user.username)
    return render(request, 'vagas/listar_inscricoes.html', {'inscricoes': inscricoes})

# Excluir inscrição
@login_required
def excluir_inscricao(request, id):
    inscricao = get_object_or_404(Inscricao, id=id)
    inscricao.delete()
    messages.success(request, 'Inscrição excluída com sucesso!')
    return redirect('listar_inscricoes')

# Candidatar-se a uma vaga
@login_required
def candidatar_se(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.vaga = vaga
            inscricao.usuario = request.user.username
            inscricao.save()
            messages.success(request, 'Você se candidatou com sucesso!')
            return redirect('listar_vagas')
    else:
        form = InscricaoForm()
    return render(request, 'vagas/candidatar_se.html', {'form': form, 'vaga': vaga})

# Editar perfil
@login_required
def editar_perfil(request):
    profile = request.user.profile
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Currículo atualizado com sucesso!')
        return redirect('editar_perfil')
    return render(request, 'vagas/editar_perfil.html', {'form': form})

# Visualizar perfil
@login_required
def ver_perfil(request):
    return render(request, 'vagas/perfil.html')

# Logout
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Logout realizado com sucesso!')
    return redirect('index')

# Registro de usuários
def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('index')
    return render(request, 'vagas/register.html', {'form': form})

# Páginas adicionais
def sobre_nos(request):
    return render(request, 'vagas/sobre_nos.html')

def contato(request):
    return render(request, 'vagas/contato.html')

def termos_de_uso(request):
    return render(request, 'vagas/termos_de_uso.html')




