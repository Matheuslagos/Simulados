from django.db import models

# Create your models here.

class Questoes(models.Model):
    TextoQuestao = models.CharField(max_length=200)
    Alternativas = models.ForeignKey('Alternativas', on_delete=models.CASCADE)
    Simulados = models.ForeignKey('Simulados', on_delete=models.CASCADE)

class Alternativas(models.Model):
    certo = models.BooleanField()
    textoAlternativa = models.CharField(max_length=200)
    

class Simulados(models.Model):
    tema = models.CharField(max_length=30)
    Questoes = models.ForeignKey('Questoes', on_delete=models.CASCADE)