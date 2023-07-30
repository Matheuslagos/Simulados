from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django import forms
from itertools import groupby
from .forms import QuestaoForm, AlternativaForm
# Create your views here.

def listar_simulados(request):
    temas = Simulado.objects.values_list('tema', flat=True).distinct()
    simulados = Simulado.objects.all()

    # Verificar se o campo "tema" foi enviado no request.GET (para filtragem)
    tema_filtrado = request.GET.get('tema')

    if tema_filtrado:
        # Filtrar os simulados por tema que comece com as letras pesquisadas (case-insensitive)
        simulados = simulados.filter(tema__istartswith=tema_filtrado)

    # Ordenar os simulados por tema em ordem alfabética
    simulados = sorted(simulados, key=lambda simulado: simulado.tema)

    # Agrupar os simulados por tema usando a função groupby
    simulados_agrupados = {}
    for tema, grupo_simulados in groupby(simulados, key=lambda simulado: simulado.tema):
        simulados_agrupados[tema] = list(grupo_simulados)

    return render(request, 'listar_simulados.html', {'simulados_agrupados': simulados_agrupados, 'temas': temas})

def detalhes_simulado(request, simulado_id):
    simulado = get_object_or_404(Simulado,pk=simulado_id)
    
    return render(request, 'detalhes_simulado.html', {'simulado': simulado} )

def processar_respostas(request):
    if request.method == 'POST':
        simulado_id = request.POST.get('simulado_id')
        simulado = Simulado.objects.get(pk=simulado_id)
        total_questoes = simulado.questoes.count()

        pontuacao = 0
        pontuacao_maxima = 0
        respostas_usuario = {}

        for questao in simulado.questoes.all():
            alternativa_id = request.POST.get(f'questao_{questao.id}')
            alternativa = Alternativa.objects.get(pk=alternativa_id)

            # Verificar se a alternativa escolhida é a correta
            if alternativa.correta:
                pontuacao += questao.pontuacao

            # Somar a pontuação máxima possível para essa questão
            pontuacao_maxima += questao.pontuacao

            respostas_usuario[questao.id] = alternativa

        porcentagem_acertos = (pontuacao / pontuacao_maxima) * 100

        return render(request, 'resultado_simulado.html', {
            'simulado': simulado,
            'total_questoes': total_questoes,
            'pontuacao': pontuacao,
            'pontuacao_maxima': pontuacao_maxima,  # Adicionando a pontuação máxima ao contexto
            'porcentagem_acertos': porcentagem_acertos,
            'respostas_usuario': respostas_usuario,
        })

    return redirect('listar_simulados')

def criar_questao(request):
    if request.method == 'POST':
        questao_form = QuestaoForm(request.POST)
        alternativas_forms = [AlternativaForm(request.POST, prefix=f'alternativa_{i}') for i in range(1, 6)]

        if questao_form.is_valid() and all(af.is_valid() for af in alternativas_forms):
            # Salvar a questão
            questao = questao_form.save()

            # Processar as alternativas enviadas no formulário
            alternativas = []
            for af in alternativas_forms:
                texto_alternativa = af.cleaned_data.get('texto_alternativa')
                correta = af.cleaned_data.get('correta', False)

                # Apenas a alternativa correta será marcada como correta
                alternativa = Alternativa(texto_alternativa=texto_alternativa, correta=correta, questao=questao)
                alternativas.append(alternativa)

            # Salvar as alternativas no banco de dados
            Alternativa.objects.bulk_create(alternativas)

            return redirect('listar_simulados')

    else:
        questao_form = QuestaoForm()
        alternativas_forms = [AlternativaForm(prefix=f'alternativa_{i}') for i in range(1, 6)]

    return render(request, 'criar_questao.html', {
        'questao_form': questao_form,
        'alternativas_forms': alternativas_forms,
    })
def criar_simulado(request):
    questoes = Questao.objects.all()

    if request.method == 'POST':
        # Processar o formulário enviado para criar o simulado
        nome_simulado = request.POST.get('nome_simulado')
        tema_simulado = request.POST.get('tema_simulado')

        # Criar o simulado com o nome e tema fornecidos
        novo_simulado = Simulado.objects.create(nome=nome_simulado, tema=tema_simulado)

        # Obter as questões selecionadas pelo usuário no formulário
        questoes_selecionadas = request.POST.getlist('questoes')

        # Adicionar as questões selecionadas ao simulado
        for questao_id in questoes_selecionadas:
            try:
                questao = Questao.objects.get(pk=questao_id)
                novo_simulado.questoes.add(questao)
            except Questao.DoesNotExist:
                # Lidar com o caso em que a questão não foi encontrada
                pass

        return redirect('listar_simulados')

    return render(request, 'criar_simulado.html', {'questoes': questoes})

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