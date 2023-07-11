import pandas as pd
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

@csrf_exempt
def upload_csv(request):
    print(request.user)
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'No te creas hábil.'}, status=500)
    
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file_csv')
        api_key = request.POST.get('api_key')

        if not uploaded_file.name.endswith('.csv'):
            return JsonResponse({'message': 'Formato de archivo inválido. Solo se permiten archivos CSV.'}, status=400)

        openai.api_key = api_key
        
        # Leer y procesar el archivo CSV
        try:
            # data = pd.read_csv(uploaded_file, header=None, delimiter=';')
            
            # messages = [
            #     { 
            #         "role": "system",
            #         "content": "Se te propocionará un csv donde cada columna es viene en forma de arreglo, donde cada columna tiene un significado y un sentido que se relaciona con las demás columnas."
            #     }
            # ]

            # prompt = 'De lo siguiente {}, dame una descripción inicial de los datos, esto incluye identificar el tipo de información (por ejemplo, numérica, categórica), el rango de valores y cualquier patrón observable.'

            # for column in data.columns:
            #     values_per_column = data[column].values
            #     values_per_column = str(values_per_column.tolist())
                
            #     messages.append({ "role": "user", "content": prompt.format(values_per_column) })
            
            #     response = openai.ChatCompletion.create(
            #         model="gpt-3.5-turbo",
            #         messages=messages,
            #         max_tokens=1000,
            #         temperature=0.7,
            #     )
                
            #     formatted_response = response['choices'][0]['message']['content']
            #     messages.append({ "role": "assistant", "content": formatted_response })

            # prompt = 'De lo analizado índicame algún patrón observable entre los datos de las diferentes columnas de datos, además sugiéreme posibles análisis que se pueden realizar con los datos.'

            # messages.append({ "role": "user", "content": prompt })

            # response = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     messages=messages,
            #     max_tokens=1000,
            #     temperature=0.7,
            # )
            
            # formatted_response = response['choices'][0]['message']['content']
            # messages.append({ "role": "assistant", "content": formatted_response })

            return JsonResponse({'response': 'Archivo cargado y procesado con éxito.', "messages": [
            {
                "role": "system",
                "content": "Se te propocionará una serie de columna de datos en forma de arreglo, donde responderás de manera concisa y clara a las preguntas que se te hagan."
            },
            {
                "role": "user",
                "content": "De lo siguiente [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], dame una descripción inicial de los datos, esto incluye identificar el tipo de información (por ejemplo, numérica, categórica), el rango de valores y cualquier patrón observable."
            },
            {
                "role": "assistant",
                "content": "Los datos proporcionados son una serie de números enteros del 1 al 50. La información es numérica y el rango de valores va desde 1 hasta 50. No se observa ningún patrón específico en los datos, ya que simplemente son una secuencia ascendente de números enteros."
            },
            {
                "role": "user",
                "content": "De lo siguiente ['Alejandro', 'Ana', 'Benjamín', 'Camila', 'Carlos', 'Carolina', 'David', 'Diana', 'Eduardo', 'Elena', 'Fabio', 'Fernanda', 'Gabriel', 'Gabriela', 'Hernán', 'Isabella', 'Javier', 'Jimena', 'Juan', 'Julia', 'Leonardo', 'Liliana', 'Manuel', 'Mariana', 'Matías', 'Natalia', 'Nicolás', 'Olivia', 'Pablo', 'Patricia', 'Raúl', 'Renata', 'Ricardo', 'Romina', 'Sebastián', 'Sofía', 'Tomás', 'Valentina', 'Víctor', 'Victoria', 'Xavier', 'Ximena', 'Yahir', 'Yesenia', 'Zacarías', 'Zaira', 'Adrián', 'Alejandra', 'Bruno', 'Brenda'], dame una descripción inicial de los datos, esto incluye identificar el tipo de información (por ejemplo, numérica, categórica), el rango de valores y cualquier patrón observable."
            },
            {
                "role": "assistant",
                "content": "Los datos proporcionados son una serie de nombres de personas. La información es categórica, ya que los nombres representan categorías o etiquetas. El rango de valores abarca desde 'Alejandro' hasta 'Zaira'. No se observa ningún patrón específico en los datos, ya que son simplemente una lista de nombres en orden alfabético."
            },
            {
                "role": "user",
                "content": "De lo siguiente [35, 28, 42, 24, 56, 31, 39, 43, 29, 52, 37, 26, 33, 30, 47, 21, 44, 27, 48, 23, 36, 50, 34, 25, 32, 29, 31, 19, 41, 55, 38, 22, 46, 28, 34, 25, 27, 20, 49, 23, 40, 26, 32, 30, 45, 24, 37, 33, 39, 29], dame una descripción inicial de los datos, esto incluye identificar el tipo de información (por ejemplo, numérica, categórica), el rango de valores y cualquier patrón observable."
            },
            {
                "role": "assistant",
                "content": "Los datos proporcionados son una serie de números enteros. La información es numérica y el rango de valores va desde 19 hasta 56. No se observa un patrón específico en los datos, ya que parecen ser valores aleatorios."
            },
            {
                "role": "user",
                "content": "De lo siguiente ['70 kg', '43 kg', '85 kg', '48 kg', '72 kg', '68 kg', '75 kg', '69 kg', '42 kg', '64 kg', '77 kg', '61 kg', '80 kg', '73 kg', '66 kg', '49 kg', '55 kg', '41 kg', '67 kg', '44 kg', '49 kg', '78 kg', '76 kg', '35 kg', '41 kg', '40 kg', '68 kg', '43 kg', '67 kg', '76 kg', '72 kg', '30 kg', '74 kg', '49 kg', '83 kg', '42 kg', '45 kg', '40 kg', '57 kg', '41 kg', '67 kg', '49 kg', '81 kg', '50 kg', '66 kg', '43 kg', '68 kg', '75 kg', '69 kg', '46 kg'], dame una descripción inicial de los datos, esto incluye identificar el tipo de información (por ejemplo, numérica, categórica), el rango de valores y cualquier patrón observable."
            },
            {
                "role": "assistant",
                "content": "Los datos proporcionados son una serie de pesos expresados en kilogramos. La información es categórica, ya que los pesos representan categorías o etiquetas. El rango de valores va desde '30 kg' hasta '85 kg'. No se observa un patrón específico en los datos, ya que los pesos parecen ser valores aleatorios."
            },
            {
                "role": "user",
                "content": "De lo analizado índicame algún patrón observable entre los datos de las diferentes columnas de datos, además sugiéreme posibles análisis que se pueden realizar con los datos."
            },
            {
                "role": "assistant",
                "content": "En base a los datos proporcionados en las diferentes columnas, no se observa un patrón observable entre ellos. Cada columna representa un tipo de información diferente (números enteros, nombres de personas, pesos en kilogramos), por lo que no hay una relación directa entre los valores de las diferentes columnas.\n\nSin embargo, se pueden realizar varios análisis con los datos proporcionados en cada columna de forma individual. Algunas posibles análisis podrían ser:\n\n- Para los datos numéricos (números enteros): calcular la media, mediana y moda para obtener medidas de tendencia central y determinar si hay valores atípicos o patrones específicos en la distribución de los datos.\n- Para los datos categóricos (nombres de personas): contar la frecuencia de cada nombre para identificar los nombres más comunes o realizar análisis de agrupamiento para identificar posibles patrones en la distribución de los nombres.\n- Para los datos de pesos en kilogramos: calcular la media, mediana y desviación estándar para obtener medidas de tendencia central y dispersión de los datos. También se pueden realizar análisis de comparación entre grupos de pesos (por ejemplo, hombres vs mujeres) o análisis de correlación con otras variables (por ejemplo, altura).\n\nEstos son solo algunos ejemplos de análisis que se pueden realizar con los datos proporcionados. La elección de los análisis dependerá del objetivo y la naturaleza de los datos."
            }
        ] }, status=200)
        except Exception as e:
            return JsonResponse({'message': 'Error al procesar el archivo CSV.'}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_exempt
def user_authenticate(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Bienvenido', 'isLogged': True}, status=200)
        else:
            return JsonResponse({'message': 'Credenciales inválidas', 'isLogged': False}, status=405)
    else:
        return JsonResponse({'message': 'Método no permitido', 'isLogged': False}, status=405)
      
@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Adiós', 'isLogout': True}, status=200)