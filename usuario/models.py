from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saldo = models.FloatField()


class Transacao(models.Model):
    tipo_transacao = [('Débito', 'Débito'), ('Crédito', 'Crédito')]
    saldo_inicial = models.FloatField()
    saldo_final = models.FloatField()
    mensagem = models.CharField(max_length=80)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='extrato')
    tipo = models.CharField(choices=tipo_transacao, max_length=7)
    data = models.DateTimeField(auto_now_add=True)
