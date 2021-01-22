from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from usuario.models import Usuario, Transacao
from usuario.serializers import UsuarioSerializer, CreditoSerializer, ExtratoSerializer, DebitoSerializer
from django.http import Http404


class UsuarioList(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class UsuarioDetail(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class UsuarioDebito(generics.GenericAPIView):
    serializer_class = DebitoSerializer

    def get_object(self, pk):
        try:
            return Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        usuario = self.get_object(pk)
        serializer_usuario = UsuarioSerializer(usuario)
        serializer_debito = DebitoSerializer(data=request.data)
        debito = None
        if serializer_debito.is_valid():
            debito = serializer_debito.data.get('debito')
            saldo_atual = usuario.saldo
            novo_saldo = saldo_atual - debito
            usuario.saldo = novo_saldo
            usuario.save()
            transacao = Transacao(
                tipo='Débito',
                saldo_inicial=saldo_atual,
                saldo_final=novo_saldo,
                mensagem=f'Debitado o valor de R$ {debito}.',
                usuario=usuario)
            transacao.save()
        else:
            return Response(serializer_debito.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer_usuario.data)


class UsuarioCredito(generics.GenericAPIView):
    serializer_class = CreditoSerializer

    def get_object(self, pk):
        try:
            return Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        usuario = self.get_object(pk)
        serializer_usuario = UsuarioSerializer(usuario)
        serializer_credito = CreditoSerializer(data=request.data)
        credito = None
        if serializer_credito.is_valid():
            credito = serializer_credito.data.get('credito')
            saldo_atual = usuario.saldo
            novo_saldo = saldo_atual + credito
            usuario.saldo = novo_saldo
            usuario.save()
            transacao = Transacao(
                tipo='Crédito',
                saldo_inicial=saldo_atual,
                saldo_final=novo_saldo,
                mensagem=f'Creditado o valor de R$ {credito}.',
                usuario=usuario)
            transacao.save()
        else:
            return Response(serializer_credito.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer_usuario.data)


class UsuarioExtrato(APIView):
    def get_object(self, pk):
        try:
            return Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tipo = request.GET.get('tipo')
        usuario = self.get_object(pk)
        if tipo in ('Crédito', 'Débito'):
            extrato = Transacao.objects.filter(usuario=usuario, tipo=tipo).order_by('-id')
        else:
            extrato = Transacao.objects.filter(usuario=usuario).order_by('-id')
        extrato_serializer = ExtratoSerializer(extrato, many=True)
        return Response(extrato_serializer.data)
