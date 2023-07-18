from django.test import TestCase, RequestFactory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, AnonymousUser

from .views import upload_csv, user_authenticate, user_logout
from django.conf import settings

import json
class UploadCSVTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_upload_csv_authenticated(self):
        request = self.factory.post('upload_csv')
        request.user = AnonymousUser()
        request.session = self.client.session
        response = upload_csv(request)
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['message'], 'No te creas hábil, tienes que loguearte.')
        
    def test_upload_csv_invalid_format(self):
        csv_file = SimpleUploadedFile('data.txt', b'my,text,data', content_type='text/plain')

        data = {
            'api_key': 'YOUR_API_KEY',
            'file_csv': csv_file
        }

        request = self.factory.post('upload_csv', data)
        request.user = self.user
        response = upload_csv(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Formato de archivo inválido. Solo se permiten archivos CSV.')

    def test_upload_csv_method_not_allowed(self):
        request = self.factory.get('upload_csv')
        request.user = self.user
        response = upload_csv(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['message'], 'Método no permitido')

    def test_upload_csv_api_key_invalid(self):
        csv_content = (
            b'columna1;columna2;columna3\n'
            b'valor1;valor2;valor3\n'
            b'valor4;valor5;valor6\n'
        )

        csv_file = SimpleUploadedFile('test_file.csv', csv_content, content_type='text/csv')
        
        data = {
            'api_key': 'INVALID_API_KEY',
            'file_csv': csv_file
        }

        request = self.factory.post('upload_csv', data)
        request.user = self.user
        response = upload_csv(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['message'], 'Error al procesar el archivo CSV.')
        self.assertEqual(data['information']['type'], 'AuthenticationError')

    def test_upload_csv_success(self):
        csv_content = (
            b'perro;plomo;3 dosis\n'
            b'perro;latita;1 dosis\n'
            b'gato;duncan;3 dosis\n'
            b'perro;manchas;4 dosis\n'
            b'gato;charlie;2 dosis\n'
            b'gato;khalessi;2 dosis\n'
            b'gato;peluchin;4 dosis\n'
        )

        csv_file = SimpleUploadedFile('test_file.csv', csv_content, content_type='text/csv')
        
        data = {
            'api_key': settings.API_KEY_FOR_TESTS,
            'file_csv': csv_file
        }

        request = self.factory.post('upload_csv', data)
        request.user = self.user
        response = upload_csv(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['response'], 'Archivo cargado y procesado con éxito.')

class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_authentication_success(self):
        request = self.factory.post('user_authenticate', {'username': 'testuser', 'password': 'testpassword'})
        request.session = self.client.session
        response = user_authenticate(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['isLogged'], True)
        self.assertEqual(data['message'], 'Bienvenido')

    def test_user_authentication_failure(self):
        request = self.factory.post('user_authenticate', {'username': 'testuser', 'password': 'wrongpassword'})
        request.session = self.client.session
        response = user_authenticate(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['isLogged'], False)
        self.assertEqual(data['message'], 'Credenciales inválidas')

    def test_user_authentication_invalid_method(self):
        request = self.factory.get('user_authenticate')
        request.session = self.client.session
        response = user_authenticate(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['isLogged'], False)
        self.assertEqual(data['message'], 'Método no permitido')

    def test_user_logout(self):
        request = self.factory.post('user_logout')
        request.session = self.client.session
        response = user_logout(request)
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['isLogout'], True)
        self.assertEqual(data['message'], 'Adiós')