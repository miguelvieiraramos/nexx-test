from rest_framework import serializers
from usuario.models import Usuario


class UsuarioValidator:

    @staticmethod
    def unique_validator(username):
        usuarios = Usuario.objects.all()
        for usuario in usuarios:
            if usuario.user.username == username:
                raise serializers.ValidationError("Esse username já existe.")
        return username
