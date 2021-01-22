from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from usuario.models import Usuario, Transacao
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

    def test_model_can_create_transacao(self):
        old_count = Transacao.objects.count()
        self.usuario.save()
        Transacao.objects.create(
            saldo_inicial=1,
            saldo_final=2,
            mensagem='any message',
            usuario=self.usuario,
            tipo='Crédito')
        new_count = Transacao.objects.count()
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

    def test_api_can_list_usuarios(self):
        self.response = self.client.get('/usuarios/')
        assert self.response.status_code == status.HTTP_200_OK

    def test_api_can_validate_unique_username(self):
        self.user.save()
        self.usuario.save()
        self.response = self.client.post('/usuarios/', self.usuario_data, format='json')
        assert self.response.status_code == status.HTTP_400_BAD_REQUEST

    def test_api_can_retrieve_usuario(self):
        self.user.save()
        self.usuario.save()
        self.response = self.client.get(f'/usuarios/{self.usuario.id}/', format='json')
        assert self.response.status_code == status.HTTP_200_OK

    def test_api_can_creditar(self):
        self.user.save()
        self.usuario.save()
        saldo_atual = self.usuario.saldo
        credito_data = {"credito": 200}
        self.response = self.client.post(f'/usuarios/{self.usuario.id}/creditar/', credito_data, format='json')
        novo_saldo = self.response.json().get('saldo')
        assert novo_saldo == saldo_atual + credito_data.get('credito')

    def test_api_can_error_not_found_creditar(self):
        credito_data = {"credito": 200}
        self.response = self.client.post('/usuarios/90/creditar/', credito_data, format='json')
        assert self.response.status_code == status.HTTP_404_NOT_FOUND

    def test_api_can_error_credito_less_1_creditar(self):
        self.user.save()
        self.usuario.save()
        credito_data = {"credito": 0}
        self.response = self.client.post(f'/usuarios/{self.usuario.id}/creditar/', credito_data, format='json')
        assert self.response.status_code == status.HTTP_400_BAD_REQUEST

    def test_api_can_debitar(self):
        self.user.save()
        self.usuario.save()
        saldo_atual = self.usuario.saldo
        debito_data = {"debito": 150}
        self.response = self.client.post(f'/usuarios/{self.usuario.id}/debitar/', debito_data, format='json')
        novo_saldo = self.response.json().get('saldo')
        assert novo_saldo == saldo_atual - debito_data.get('debito')

    def test_api_can_error_not_found_debitar(self):
        debito_data = {"debito": 200}
        self.response = self.client.post('/usuarios/90/debitar/', debito_data, format='json')
        assert self.response.status_code == status.HTTP_404_NOT_FOUND

    def test_api_can_error_credito_less_1_debitar(self):
        self.user.save()
        self.usuario.save()
        debito_data = {"debito": 0}
        self.response = self.client.post(f'/usuarios/{self.usuario.id}/debitar/', debito_data, format='json')
        assert self.response.status_code == status.HTTP_400_BAD_REQUEST

    def test_api_can_list_extrato(self):
        self.user.save()
        self.usuario.save()
        transacao = Transacao(
                tipo='Crédito',
                saldo_inicial=100,
                saldo_final=200,
                mensagem='Creditado o valor de R$ 100.',
                usuario=self.usuario)
        transacao.save()
        self.response = self.client.get(f'/usuarios/{self.usuario.id}/extrato/')
        self.response.status_code == status.HTTP_200_OK

    def test_api_can_error_not_found_extrato(self):
        self.response = self.client.get('/usuarios/1/extrato/')
        self.response.status_code == status.HTTP_404_NOT_FOUND

    def test_api_can_filter_extrato(self):
        self.user.save()
        self.usuario.save()
        transacao = Transacao(
                tipo='Crédito',
                saldo_inicial=100,
                saldo_final=200,
                mensagem='Creditado o valor de R$ 100.',
                usuario=self.usuario)
        transacao.save()
        self.response = self.client.get(f'/usuarios/{self.usuario.id}/extrato/?tipo=Crédito')
        self.response.status_code == status.HTTP_200_OK
