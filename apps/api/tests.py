from django.test import TestCase
from django.urls import reverse
from django.test import RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
import json

from .views import upload_csv

class UploadCSVTestCase(TestCase):

    def test_error_processing_csv(self):
        request_factory = RequestFactory()
        url = reverse('upload_csv')
        
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

        request = request_factory.post(url, data=data)
        request.FILES['file_csv'] = csv_file
        
        # Realizar la solicitud POST
        response = upload_csv(request)
        
        content = response.content.decode("utf-8")
        data = json.loads(content)
    
        # # Comprueba el resultado esperado
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['message'], 'Error al procesar el archivo CSV.')
