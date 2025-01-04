from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import VagaForm, InscricaoForm
from .models import Vaga, Inscricao

# Página inicial
def index(request):
    total_vagas = Vaga.objects.count()
    total_inscricoes = Inscricao.objects.count()
    return render(request, 'vagas/index.html', {'total_vagas': total_vagas, 'total_inscricoes': total_inscricoes})

# Listar vagas
def listar_vagas(request):
    query = request.GET.get('q')
    if query:
        vagas = Vaga.objects.filter(titulo__icontains=query)
    else:
        vagas = Vaga.objects.all()

    paginator = Paginator(vagas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vagas/listar_vagas.html', {'page_obj': page_obj, 'query': query})

# Criar vaga
@login_required
def criar_vaga(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaga criada com sucesso!')
            return redirect('listar_vagas')
        else:
            messages.error(request, 'Erro ao criar a vaga. Verifique os dados informados.')
    else:
        form = VagaForm()
    return render(request, 'vagas/criar_vaga.html', {'form': form})

# Editar vaga
@login_required
def editar_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    if request.method == 'POST':
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaga atualizada com sucesso!')
            return redirect('listar_vagas')
        else:
            messages.error(request, 'Erro ao atualizar a vaga. Verifique os dados informados.')
    else:
        form = VagaForm(instance=vaga)
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
    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.vaga = vaga
            inscricao.save()
            messages.success(request, 'Inscrição realizada com sucesso!')
            return redirect('listar_vagas')
        else:
            messages.error(request, 'Erro ao realizar a inscrição.')
    else:
        form = InscricaoForm()
    return render(request, 'vagas/inscrever.html', {'form': form, 'vaga': vaga})

# Listar inscrições
@login_required
def listar_inscricoes(request):
    inscricoes = Inscricao.objects.select_related('vaga').all()
    return render(request, 'vagas/listar_inscricoes.html', {'inscricoes': inscricoes})

# Excluir inscrição
@login_required
def excluir_inscricao(request, id):
    inscricao = get_object_or_404(Inscricao, id=id)
    inscricao.delete()
    messages.success(request, 'Inscrição excluída com sucesso!')
    return redirect('inscricoes')

# Logout personalizado
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Logout realizado com sucesso!')
        return redirect('index')

# Página "Sobre Nós"
def sobre_nos(request):
    return render(request, 'vagas/sobre_nos.html')

# Página "Contato"
def contato(request):
    return render(request, 'vagas/contato.html')

# Página "Termos de Uso"
def termos_de_uso(request):
    return render(request, 'vagas/termos_de_uso.html')
