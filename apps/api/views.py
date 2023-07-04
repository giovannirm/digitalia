import pandas as pd
import csv
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_csv(request):
        
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file_csv')
        api_key = request.POST.get('api_key')

        if not uploaded_file.name.endswith('.csv'):
            return JsonResponse({'message': 'Formato de archivo inválido. Solo se permiten archivos CSV.'}, status=400)

        openai.api_key = api_key
        
        # Leer y procesar el archivo CSV
        try:
            data = pd.read_csv(uploaded_file, header=None, delimiter=';')
            
            messages = [
                { 
                    "role": "system",
                    "content": "Se te propocionará un csv donde cada columna es viene en forma de arreglo, donde cada columna tiene un significado y un sentido que se relaciona con las demás columnas."
                }
            ]

            prompt = 'De lo siguiente {}, dame una descripción inicial de los datos, esto incluye identificar el tipo de información (por ejemplo, numérica, categórica), el rango de valores y cualquier patrón observable.'

            for column in data.columns:
                values_per_column = data[column].values
                values_per_column = str(values_per_column.tolist())
                print(values_per_column)
                messages.append({ "role": "user", "content": prompt.format(values_per_column) })
            
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7,
                )
                
                formatted_response = response['choices'][0]['message']['content']
                messages.append({ "role": "assistant", "content": formatted_response })

            prompt = 'De lo analizado índicame algún patrón observable entre los datos de las diferentes columnas de datos, además sugiéreme posibles análisis que se pueden realizar con los datos.'

            messages.append({ "role": "user", "content": prompt })

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
            )
            
            formatted_response = response['choices'][0]['message']['content']
            messages.append({ "role": "assistant", "content": formatted_response })

            context = {
                "messages": messages
            }

            return JsonResponse({'response': 'Archivo cargado y procesado con éxito.', "messages": context }, status=200)
        except Exception as e:
            return JsonResponse({'message': 'Error al procesar el archivo CSV.'}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)