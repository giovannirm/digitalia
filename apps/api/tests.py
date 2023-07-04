from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

from .views import upload_csv

class UploadCSVTestCase(TestCase):

    def test_my_function(self):
        client = Client()
        url = reverse('http://127.0.0.1:8000/v1/api/upload-csv/')

        # Los parámetros de la solicitud POST
        data = {
            'api_key': 'YOUR_API_KEY',
        }

        csv_content = (
            b'columna1;columna2;columna3\n'
            b'valor1;valor2;valor3\n'
            b'valor4;valor5;valor6\n'
        )

        csv_file = SimpleUploadedFile('test_file.csv', csv_content, content_type='text/csv')

        data = {
            'param1': 'valor1',
        }

        files = {
            'file_param': csv_file,
        }

        response = client.post(url, data, files)

        # Comprueba el resultado esperado
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['result'], 'Error al procesar el archivo CSV.')