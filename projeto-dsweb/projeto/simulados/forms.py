from django import forms
from .models import Questao, Alternativa

class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = ['texto_questao', 'pontuacao']

class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = ['texto_alternativa', 'correta']