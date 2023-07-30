from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.

def listarSimuladosView(request):
    temas = Simulado.objects.values_list('tema', flat=True).distinct()
    simulados = Simulado.objects.all()
    tema_filtrado = request.GET.get('tema')

    if tema_filtrado:
        simulados = simulados.filter(tema=tema_filtrado)

    return render(request, 'listar_simulados.html', {'simulados': simulados, 'temas': temas})

def detalhes_simulado(request, simulado_id):
    simulado = get_object_or_404(Simulado,pk=simulado_id)
    
    return render(request, 'detalhes_simulado.html', {'simulado': simulado} )

