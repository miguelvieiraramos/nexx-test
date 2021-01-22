from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from usuario.models import Usuario
from django.contrib.auth.models import User


class ModelTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='Foo', email='foo@email.com')
        user.set_password('any_password')
        self.usuario = Usuario(user=user, saldo=200)

    def test_model_can_create_usuario(self):
        old_count = Usuario.objects.count()
        self.usuario.save()
        new_count = Usuario.objects.count()
        assert old_count != new_count


class ViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.usuario_data = {'username': 'foo', 'email': 'foo@email.com', 'password': 'any_password', 'saldo': 200}
        self.user = User(username='foo', email='foo@email.com')
        self.user.set_password('any_password')
        self.usuario = Usuario(user=self.user, saldo=200)

    def test_api_can_create_usuario(self):
        self.response = self.client.post('/usuarios/', self.usuario_data, format='json')
        assert self.response.status_code == status.HTTP_201_CREATED

    def test_api_can_list_all_usuarios(self):
        self.response = self.client.get('/usuarios/')
        assert self.response.status_code == status.HTTP_200_OK

    def test_unique_username_validator(self):
        self.user.save()
        self.usuario.save()
        self.response = self.client.post('/usuarios/', self.usuario_data, format='json')
        assert self.response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_api_can_retrieve_usuario(self):
        self.user.save()
        self.usuario.save()
        self.response = self.client.get(f'/usuarios/{self.usuario.id}/', format='json')
        assert self.response.status_code == status.HTTP_200_OK

    def test_api_can_add_to_saldo(self):
        self.user.save()
        self.usuario.save()
        saldo_atual = self.usuario.saldo
        credito_data = {"credito": 200}
        self.response = self.client.post(f'/usuarios/{self.usuario.id}/creditar/', credito_data, format='json')
        novo_saldo = self.response.json().get('saldo')
        assert novo_saldo == saldo_atual + credito_data.get('credito')
    
    def test_api_error_usuario_does_not_exist(self):
        credito_data = {"credito": 200}
        self.response = self.client.post(f'/usuarios/90/creditar/', credito_data, format='json')
        assert self.response.status_code == status.HTTP_404_NOT_FOUND

    def test_api_error_when_saldo_less_than_1(self):
        self.user.save()
        self.usuario.save()
        saldo_atual = self.usuario.saldo
        credito_data = {"credito": 0}
        self.response = self.client.post(f'/usuarios/{self.usuario.id}/creditar/', credito_data, format='json')
        assert self.response.status_code == status.HTTP_400_BAD_REQUEST