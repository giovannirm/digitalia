from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from api.models import Shipment, Message
from api.constants import ROLES

import pandas as pd
import openai
import tiktoken

@csrf_exempt
def upload_csv(request):    
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'No te creas hábil, tienes que loguearte.'}, status=500)
    
    if request.method == 'POST':
  
        uploaded_file = request.FILES.get('file_csv')
        api_key = request.POST.get('api_key')

        if not uploaded_file.name.endswith('.csv'):
            return JsonResponse({'message': 'Formato de archivo inválido. Solo se permiten archivos CSV.'}, status=400)

        openai.api_key = api_key
        
        # Leer y procesar el archivo CSV
        try:
            data = pd.read_csv(uploaded_file, header=None, delimiter=';')
            
            MODEL = 'gpt-3.5-turbo'
            LIMIT_TOKENS = 4097
            TEMPERATURE = 0.7
            
            MAX_TOKENS = 500

            # Constante para indicar si el prompt se debe dividir en varios mensajes
            # WILL_CRUMBLE = True

            messages = [
                {
                    'role': 'system',
                    'content': 'Se te propocionará un csv donde cada columna es viene en forma de arreglo, donde cada columna tiene un significado y un sentido que se relaciona con las demás columnas.'
                }
            ]

            prompt = 'De lo siguiente {}, dame una descripción inicial de los datos, esto incluye identificar el tipo de información (por ejemplo, numérica, categórica), el rango de valores y cualquier patrón observable.'

            for column in data.columns:
                values_per_column = data[column].values
                values_per_column = str(values_per_column.tolist())
                
                messages.append({ 'role': 'user', 'content': prompt.format(values_per_column) })
                
                total_tokens = num_tokens_from_messages(messages=messages)
                if total_tokens < LIMIT_TOKENS:
                    response = openai.ChatCompletion.create(
                        model=MODEL,
                        messages=messages,
                        max_tokens=MAX_TOKENS,
                        temperature=TEMPERATURE,
                    )
                    
                    formatted_response = response['choices'][0]['message']['content']
                    messages.append({ 'role': 'assistant', 'content': formatted_response })

                # elif WILL_CRUMBLE:
                #     encoding = tiktoken.encoding_for_model(MODEL)
                #     CHUNK_SIZE = 3000
                #     chunks = []    14500
                #     for i in range(0, total_tokens, CHUNK_SIZE):
                #         chunks.append(encode[i:i+CHUNK_SIZE])
                    
                #     final_response = []
                #     for index, chunk in enumerate(chunks):
                #         response = openai.ChatCompletion.create(
                #             model=MODEL,
                #             messages=encoding.decode(chunk),
                #             temperature=TEMPERATURE,
                #             max_tokens=MAX_TOKENS,
                #         )
                #         final_response.append(response['choices'][0]['message']['content'])

                    
                #     print(final_response)


                else:
                    return JsonResponse({'message': f'Error interno. Cuota: {total_tokens}, Límite: {LIMIT_TOKENS}. Excede el límite de tokens permitido'}, status=200)

            prompt = 'De lo analizado índicame algún patrón observable entre los datos de las diferentes columnas de datos, además sugiéreme posibles análisis que se pueden realizar con los datos.'

            messages.append({ "role": "user", "content": prompt })
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=messages,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
            )
            
            formatted_response = response['choices'][0]['message']['content']
            messages.append({ "role": "assistant", "content": formatted_response })
            
            # Invirtiendo el diccionario de roles para obtener el identificador a partir de la descripción
            roles_dict = dict((description, identifier) for identifier, description in ROLES)

            shipment = Shipment(user_id = request.user.id, state='C')
            shipment.save()
            insert_id = shipment.id
            
            for mssg in messages:
                response = Message(
                    role = roles_dict.get(mssg.get('role')),
                    message = mssg.get('content'),
                    shipment_id = insert_id
                )
                response.save()
       
            return JsonResponse({'response': 'Archivo cargado y procesado con éxito.', 'messages': messages}, status=200)
        except Exception as e:
            shipment = Shipment(user_id = request.user.id , state='F')
            shipment.save()
            exception_data = {
                'type': type(e).__name__,
                'message': str(e)
            }

            return JsonResponse({'message': 'Error al procesar el archivo CSV.', 'information': exception_data}, status=500)
        
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
            return JsonResponse({'message': 'Credenciales inválidas', 'isLogged': False}, status=200)
    else:
        return JsonResponse({'message': 'Método no permitido', 'isLogged': False}, status=200)
      
@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Adiós', 'isLogout': True}, status=200)
    else:
        return JsonResponse({'message': 'Método no permitido', 'isLogout': False}, status=200)

def num_tokens_from_messages(messages):
    model = 'gpt-3.5-turbo'
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens_per_message = 4
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value)) 
    num_tokens += 2
    return num_tokens