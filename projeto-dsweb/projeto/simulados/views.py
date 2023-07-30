from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
# Create your views here.

def listarSimuladosView(request):
    temas = Simulado.objects.values_list('tema', flat=True).distinct()
    simulados = Simulado.objects.all()
    tema_filtrado = request.GET.get('tema')

    if tema_filtrado:
        simulados = simulados.filter(tema__istartswith=tema_filtrado)

    return render(request, 'listar_simulados.html', {'simulados': simulados, 'temas': temas})

def detalhes_simulado(request, simulado_id):
    simulado = get_object_or_404(Simulado,pk=simulado_id)
    
    return render(request, 'detalhes_simulado.html', {'simulado': simulado} )

def processar_respostas(request):
    if request.method == 'POST':
        simulado_id = request.POST.get('simulado_id')
        simulado = Simulado.objects.get(pk=simulado_id)
        total_questoes = simulado.questoes.count()

        pontuacao = 0
        respostas_usuario = {}

        for questao in simulado.questoes.all():
            alternativa_id = request.POST.get(f'questao_{questao.id}')
            alternativa = Alternativa.objects.get(pk=alternativa_id)

            # Verificar se a alternativa escolhida é a correta
            if alternativa.correta:
                pontuacao += questao.pontuacao

            respostas_usuario[questao.id] = alternativa

        porcentagem_acertos = (pontuacao / (total_questoes * questao.pontuacao)) * 100

        return render(request, 'resultado_simulado.html', {
            'simulado': simulado,
            'total_questoes': total_questoes,
            'pontuacao': pontuacao,
            'porcentagem_acertos': porcentagem_acertos,
            'respostas_usuario': respostas_usuario,
        })

    return redirect('listar_simulados')

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm() 

    return render(request, 'cadastro.html', {'form': form})

def login_view(request):
    return auth_views.LoginView.as_view(template_name='login.html')(request)
def logout_view(request):
    logout(request)
    return redirect('listar_simulados')