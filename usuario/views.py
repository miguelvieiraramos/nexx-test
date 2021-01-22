from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from usuario.models import Usuario
from usuario.serializers import UsuarioSerializer, CreditoSerializer
from django.http import Http404


class UsuarioList(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class UsuarioDetail(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class UsuarioCredito(APIView):
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
        else:
            return Response(serializer_credito.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer_usuario.data)
