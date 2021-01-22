from rest_framework import serializers
from usuario.models import Usuario
from django.contrib.auth.models import User
from usuario.validators import UsuarioValidator


class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',
                                     required=True,
                                     validators=[UsuarioValidator.unique_validator])
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(write_only=True, source='user.password')
    saldo = serializers.FloatField()

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'saldo']

    def create(self, validated_data):
        user = User.objects.create(
          username=validated_data['user']['username'],
          email=validated_data['user']['email']
        )
        user.set_password(validated_data['user']['password'])
        return Usuario.objects.create(user=user, saldo=validated_data.get('saldo'))
