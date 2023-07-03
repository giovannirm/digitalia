import pandas as pd
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        api_key = request.POST.get('api_key')
        
        if not uploaded_file.name.endswith('.csv'):
            return JsonResponse({'message': 'Formato de archivo inválido. Solo se permiten archivos CSV.'}, status=400)

        openai.api_key = api_key
        
        # Leer y procesar el archivo CSV
        try:
            data = pd.read_csv(uploaded_file, header=None, delimiter=';')

            request.session["messages"] = [
                { 
                    "role": "system",
                    "content": "Se te propocionará una serie de columna de datos en forma de arreglo, donde responderás de manera concisa y clara a las preguntas que se te hagan."
                }
            ]

            prompt = 'De lo siguiente {}, dame una descripción inicial de los datos, esto incluye identificar el tipo de información (por ejemplo, numérica, categórica), el rango de valores y cualquier patrón observable.'

            for column in data.columns:
                values_per_column = data[column].values
                values_per_column = str(values_per_column.tolist())
                
                request.session["messages"].append({ "role": "user", "content": prompt.format(values_per_column) })
            
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=request.session["messages"],
                    max_tokens=500,
                    temperature=0.1,
                )
                
                print("res", response)
                formatted_response = response['choices'][0]['message']['content']
                print("for", formatted_response)

            prompt = 'De lo analizado índicame algún patrón observable entre los datos de las diferentes columnas de datos, además sugiéreme posibles análisis que se pueden realizar con los datos.'

            request.session["messages"].append({ "role": "user", "content": prompt })

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session["messages"],
                max_tokens=500,
                temperature=0.1,
            )
            
            formatted_response = response['choices'][0]['message']['content']
            print("for", formatted_response)
            # consultation = 'Tengo las siguientes columnas en csv separados en array ' + consultColumns + '.' + prompt1

            # Realizar operaciones de procesamiento o extracción de datos aquí
            # Por ejemplo, utilizar los datos en ChatGPT
            
            return JsonResponse({'message': 'Archivo cargado y procesado con éxito.'})
        except Exception as e:
            return JsonResponse({'message': 'Error al procesar el archivo CSV.'}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)