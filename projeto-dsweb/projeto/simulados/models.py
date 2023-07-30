from django.db import models

# Create your models here.


class Questao(models.Model):
    texto_questao = models.CharField(max_length=200)
    pontuacao = models.IntegerField(default=1)

    def __str__(self):
        return self.texto_questao

class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='alternativas')
    texto_alternativa = models.CharField(max_length=100)
    correta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto_alternativa

class Simulado(models.Model):
    nome = models.CharField(max_length=100)
    questoes = models.ManyToManyField(Questao)
    tema = models.CharField(max_length=50, default='Tema')

    def __str__(self):
        return self.nome