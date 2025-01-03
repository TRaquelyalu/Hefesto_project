from django.shortcuts import render, redirect, get_object_or_404
from .forms import VagaForm
from .models import Vaga  # Certifique-se de que o modelo Vaga já está criado e migrado
from django.core.paginator import Paginator
from .forms import InscricaoForm  # Certifique-se de que o formulário está importado

def inscrever(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)  # Busca a vaga pelo ID ou retorna 404
    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        if form.is_valid():
            inscricao = form.save(commit=False)  # Salva o formulário sem enviar ao banco
            inscricao.vaga = vaga  # Relaciona a inscrição à vaga
            inscricao.save()  # Salva no banco de dados
            return redirect('listar_vagas')  # Redireciona para a página de listagem
    else:
        form = InscricaoForm()  # Cria um formulário vazio
    return render(request, 'vagas/inscrever.html', {'form': form, 'vaga': vaga})


def listar_vagas(request):
    query = request.GET.get('q')  # Obtém o termo digitado no campo de busca
    if query:
        vagas = Vaga.objects.filter(titulo__icontains=query)  # Filtra vagas pelo título
    else:
        vagas = Vaga.objects.all()  # Mostra todas as vagas

    # Paginação
    paginator = Paginator(vagas, 5)  # Mostra 5 vagas por página
    page_number = request.GET.get('page')  # Obtém o número da página atual
    page_obj = paginator.get_page(page_number)  # Recupera os objetos da página atual

    return render(request, 'vagas/listar_vagas.html', {'page_obj': page_obj, 'query': query})


# View para a página inicial
def index(request):
    # Certifique-se de que o template 'vagas/base.html' existe e está configurado corretamente
    return render(request, 'vagas/base.html')

# View para criar uma nova vaga
def criar_vaga(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redireciona para a página inicial
    else:
        form = VagaForm()
    return render(request, 'vagas/criar_vaga.html', {'form': form})  # Certifique-se de que o template existe

# View para editar uma vaga existente
def editar_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)  # Busca a vaga pelo ID
    if request.method == 'POST':
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redireciona para a página inicial
    else:
        form = VagaForm(instance=vaga)  # Preenche o formulário com os dados da vaga
    return render(request, 'vagas/editar_vaga.html', {'form': form})

# View para excluir uma vaga
def excluir_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)  # Busca a vaga pelo ID
    vaga.delete()  # Exclui a vaga
    return redirect('index')  # Redireciona para a página inicial

