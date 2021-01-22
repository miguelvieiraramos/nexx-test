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

    def test_api_can_create_usuario(self):
        self.response = self.client.post('/usuarios/', self.usuario_data, format='json')
        assert self.response.status_code == status.HTTP_201_CREATED
    

    def test_api_can_list_all_usuarios(self):
      self.response = self.client.get('/usuarios/')
      assert self.response.status_code == status.HTTP_200_OK
