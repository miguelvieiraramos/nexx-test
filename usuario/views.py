from rest_framework import generics
from usuario.models import Usuario
from usuario.serializers import UsuarioSerializer


class UsuarioList(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
