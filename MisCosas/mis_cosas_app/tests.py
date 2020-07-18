from django.test import TestCase
from . import views
from django.contrib.auth.models import User
# Create your tests here.
class TestHTTP(TestCase):

    def test_get_home(self):
        respuesta = self.client.get('/')
        self.assertEqual(respuesta.status_code, 200)

    def test_get_login(self):
        respuesta = self.client.get('/login')
        self.assertEqual(respuesta.status_code, 200)

    def test_get_info(self):
        respuesta = self.client.get('/info')
        self.assertEqual(respuesta.status_code, 200)

    def test_get_logout(self):
        respuesta = self.client.get('/logout')
        self.assertEqual(respuesta.status_code, 302)

    def test_get_usuarios(self):
        respuesta = self.client.get('/usuarios')
        self.assertEqual(respuesta.status_code, 200)

    def test_get_registro(self):
        respuesta = self.client.get('/registro')
        self.assertEqual(respuesta.status_code, 200)

    def test_get_alimentadores(self):
        respuesta = self.client.get('/alimentadores')
        self.assertEqual(respuesta.status_code, 200)
