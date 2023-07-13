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

            # messages = []

            prompt = 'De lo siguiente {}, dame una descripción inicial de los datos, esto incluye identificar el tipo de información (por ejemplo, numérica, categórica), el rango de valores y cualquier patrón observable.'

            # for i in range(1):
            for column in data.columns:
                values_per_column = data[column].values
                values_per_column = str(values_per_column.tolist())
                
                messages.append({ 'role': 'user', 'content': prompt.format(values_per_column) })

                # Forzar error si se excede el límite de tokens
                # messages.append({ 'role': 'user', 'content': """Dame un resumen de la siguiente historia: Dame un resumen  de la siguiente historia EL CASERO (retratos del lado oscuro) I. INTROITO Soy licenciado en Historia, soy diplomado en Magisterio, he trabajado en la enseñanza pública y en la privada, he hecho cursillos, he hecho novillos y hasta he hecho ganchillo, y he hecho mil cosas más, pero, ante todo, soy casero. No, no me refiero con ello a que haya sentido la llamada de la vocación arbitral y juzgue con excesiva benevolencia a los equipos que juegan en su propio feudo (aunque he de reconocer que el fútbol es la mayor de mis aficiones y desde pequeño he sido fiel seguidor de mi equipo local). Y tampoco quiero decir que sea afecto a permanecer todo el día en mi humilde morada, sin salir apenas (aunque no salgo todo lo que yo quisiera, en parte porque no me dejan). No, nada de eso. Con la palabra casero  quiero expresar mi condición -humana, al fin y al cabo- de copropietario de bienes inmuebles arrendados a inquilinos diversos (y perversos, como más tarde se verá). Y es esta ocupación -que algunos creerán morosa, usurera y cruel- la causa de gran parte de las desdichas que diré y de pesadillas que cada vez se están haciendo más pesadas. Quiso la Fortuna que mi familia poseyera en la postguerra algunos edificios en una estrecha calle de una selecta zona de la ciudad, llamada Ensanche  -aunque no sé si el término incluía a nuestra angosta calle- a imitación del Eixample barcelonés, porque todo lo que hacemos en esta ciudad es imitar mal a los demás. Pero igualmente quiso la Fortuna, que no sólo es ciega sino a veces aciaga, que nos viéramos obligados (bueno, yo no, porque aún no había nacido), por la delicada situación postbélica, a alquilar los pisos de uno de esos edificios a familias modestas pero ejemplares. O al menos eso era lo que pensaban mis mayores, pues estaban muy adelantados para aquella época y ya pedían estrictas referencias a los aspirantes a inquilinos (como vemos en las películas, cuando buscan a una institutriz inglesa). Los que superaban el casting -perdón, la entrevista- tenían acceso a uno de aquellos pisos, porque la vivienda -y todo lo demás- se había puesto muy difícil en aquella época. Y como entonces España no iba tan bien como ahora (aunque los gestores de la cosa pública llevaran los mismos apellidos), se fijaron unos alquileres asequibles, es decir, irrisorios. Pero como el contrato no preveía posteriores subidas, la risa fue para los inquilinos, que se encontraron durante años con viviendas supremas a precios ínfimos. Esta situación ha seguido su curso hasta ahora y somos las nuevas generaciones de la familia las que colaboramos en las ingratas tareas de recaudación. Por su parte, los inquilinos también han cedido su paso a nuevas generaciones, pero a diferencia de las nuestras, aquellas evidencian un notable declive de la raza y no hubieran pasado bajo ningún concepto el estricto casting  de antaño. De todas formas, también hay que reconocer que algunos de los inquilinos primigenios no han resultado ser tan buenas personas como parecían, bien porque se han ido degenerando con la edad y por el trato con sus hijos, bien porque nuestros mayores no disponían de una máquina de la verdad  y se creyeron más mentiras que en una campaña electoral. Y para complicar el asunto, los viejos inquilinos nunca mueren (¡ojalá hubieran sido rockeros, que siempre la palman pronto!) y no podemos reemplazarlos por otros nuevos que firmen un contrato de alquiler adaptado a los tiempos y dineros que corren. Y por cuatro duros (bueno, el pico son diecinueve pesetas y nunca nos perdonan la diminuta peseta, aunque se tengan que poner la gafas de ver) tenemos que seguir porfiando con esta gente para que nos pague el alquiler de estos bienes inmuebles  que poseemos (porque si fueran móviles  -como todo lo de ahora- a buen seguro que habríamos llevado el edificio al borde de un acantilado para abandonarlo allí o dejarlo caer cuan largo era, como en las películas de suspense, donde todo pende de un delgado hilo fatuo y al final se despeña sin remisión). Habrá pensado el lector que exagero, que no estoy en mis cabales, que soy un sádico que hace sufrir a los demás y luego se complace en rememorar sus hazañas, o que soy un masoquista que disfruta sufriendo para recolectar una ínfima cantidad de dinero o, en fin, que estos peculiares inquilinos me han ablandado los sesos como los requesones se lo hicieron a Don Quijote. Pues puede que sí, pero lo cierto es que cada visita a aquel edificio causa en mí una honda impresión. Y de nuevo puede pensar el lector que exagero, pues esta tarea recaudatoria sólo tiene lugar una vez cada dos meses. A pesar de ello, el impacto es tal (y eso que aún no me han tirado ningún objeto contundente) que me deja varias semanas en un estado catatónico y psicótico, y cuando empiezo a sentirme aliviado de estos horribles síntomas ya han pasado los dos meses y tengo que volver, sintiéndome como un humilde peón en manos del mito del eterno retorno. Lo único que consigue mitigar la inminente llegada de la fecha aciaga es que mi familia es numerosa y nos turnamos en esta tarea recaudatoria para no quebrantar en exceso la salud mental de padres y hermanos. Aún así, ocurre con frecuencia que muchos de mis hermanos se escaquean con excusas dudosas y me toca a mí bailar con los más feos. Así pues, recordemos que este repetitivo rito iniciático (bueno, son tantas veces que ya somos unos maestros... o maestres ) de descenso en el Averno (para situarme, siempre releo el final de la Divina Commedia  antes de ir allí, por si falla el ascensor) que tan insalubres secuelas me produce, tiene lugar un día (sin duda, el día más largo) en el que dos miembros de la familia (como hemos dicho, yo soy casi siempre titular en las alineaciones), como si fuéramos una pareja de la guardia civil (incluso este cuerpo podría salir descabezado y mutilado de allí, para que el lector se haga una idea de lo que vamos a encontrar), nos dirigimos al vetusto edificio, que a nuestra vista (y no digamos a la de Don Quijote) se transforma en el más siniestro castillo que pueda uno imaginar. He dicho que vamos en parejas y es siempre así por varias razones. Primero, por el más elemental instinto de supervivencia. Segundo, porque nos permite representar un ardid teatral que parece haber impresionado a algunos de los inquilinos, y hay que explotar hasta el máximo esta pequeña victoria en tan gran guerra. En efecto, como mis hermanos y yo vivimos los conflictivos años de la adolescencia en los conflictivos años setenta, tenemos interiorizados en nuestra consciencia los patrones de comportamiento ilustrados por los telefilmes de la época. Entre ellos abundaban los de signo policíaco, donde era frecuente ver parejas de policías que ejercitaban con los raterillos (porque con los peces gordos no se atrevían) un ardid dual, esquizoide, maniqueo, bífido y carnavalesco, fértil simbiosis de contrarios que hoy recibiría sin duda el apelativo de bicefalia : el de policía malo  -irascible, visceral, de mano (y más cosas) tonta- y policía bueno  -comprensivo, tolerante, amigo de tratos y desfacedor de los entuertos que estaba a punto de cometer su compañero. He de advertir al lector que yo siempre desempeñaba el papel de policía bueno, cosa que me exasperaba aún más ante estos siniestros inquilinos. Ahora bien, lo que nunca acabé de comprender es que los inquilinos pensaran que me dedicaba a la abogacía, pues nunca he asociado este oficio con los buenos oficios del policía bueno. Pero para no entretener al estresado lector con más preliminares, y aprovechando que hace justo dos meses que fuimos a cobrar, le invito a que nos acompañe a esta peculiar casa de los horrores, lo más bajo de la zona alta de la ciudad. Aunque advierto al lector (y el que avisa no es traidor) que esta visita puede agravarles el ya agudo estrés que padecen algunos y, aún más, puede producirles (aunque en casos aislados, como se dice siempre que hay una epidemia) insomnio, úlcera gastroduodenal, jaqueca, hidrofobia, polisemia, parasíntesis, filatelia y serios trastornos de la personalidad. Ahora bien, si quiere acompañarnos, hágalo bajo su completa responsabilidad, coja el chaleco antibalas y el casco de albañil y ahí vamos. II. “LOS MARCAPASOS” En el primero derecha, vivían doña Águeda y don Cecilio, dos venerables ancianos más conocidos entre sus vecinos como los marcapasos. Tenía este apodo el origen en que ambos llevaban implantado este mecanismo para intentar frenar el envejecimiento de sendos corazones que estaban empezando a querer dejar de latir. Porque si de algo pecaban doña Águeda y don Cecilio -siempre muy amables con todos los vecinos y aun con nosotros- era de anhelar la inmortalidad, de su empecinada obstinación por resistirse al inexorable paso del tiempo. Cuentan que doña Águeda y don Cecilio fueron en sus tiempos mozos atractiva pareja de cantantes y bailarines que gozó de cierta fama. Actuaban para público selecto, para extranjeros (fueron de los primeros en cantar en inglés, razón por la que nosotros también los llamábamos los pacemakers) y hasta grabaron un disco y actuaron en varias películas. Decían que fueron geniales, los mejores sin duda, en diversos géneros: canción española, bailes tropicales, flamenco, tap-dancing  a lo Fred Astaire, cabaret de entreguerras, canción melódica francesa y hasta algo del primer rock. Pero lo bueno como viene se va, y tras veinte años de intensa dedicación artística, doña Águeda y don Cecilio empezaron a habitar en el olvido de los empresarios de espectáculos: su apoderado (en esa época aún no se llamaban managers) los dejó por otra pareja artística, mediocre pero más joven; el público empezó a darles la espalda y a quejarse de que siempre hacían los mismos números; y los empresarios mismos, aunque los halagaban con vanas palabras, en el último momento no los contrataban. Y el dinero que ganaron se fue como habían vivido: deprisa. Y, a diferencia de otros muchos de su gremio, ellos no se quedaron en la calle sino en uno de nuestros pisos, pues nuestros mayores -grandes seguidores de la pareja (aún no se llamaban fans, pues era gente cuerda)- se apiadaron de ellos y les concedieron el alquiler de un piso del edificio. Situados en una posición algo menos dramática de la que parecía augurar su prematura caída, doña Águeda y don Cecilio se rehicieron. Aprovecharon su ubicación en un barrio con clase para dedicarse a dar clases de canto y baile a los hijos e hijas de familias pudientes que adoraron a la pareja en su tiempo de gloria. Y todo esto les animó a no envejecer. Él iba siempre impecablemente vestido, con trajes de crooner  o chanteur  a lo Frank Sinatra, Maurice Chevalier o Yves Montand, con sombrero de music-hall y bastón labrado, y hasta se atrevía con mallas de baile, como si fuera a participar en un decadente remake de Cabaret. Pero ella no le iba a la zaga: aún trataba de lucir vestidos ajustados y provocadores que ella llamaba, con una nueva palabra aprendida, sexys; o bien se exhibía con vaporosos tules y aparatosos foulards; disimulaba vanamente sus innumerables arrugas con kilos de maquillaje; llevaba siempre el cabello tintado de rubio platino; y si no se hizo la cirugía estética, sin duda fue por falta de dinero. Con esa apariencia, no es de extrañar que entre los restantes inquilinos -siempre prestos a poner apodos cinematográficos a sus vecinos, como iremos viendo- doña Águeda se ganara, a pulso, el apelativo de Gloria Swanson: el paradigma de la actriz, cantante o bailarina en decadencia, por todos olvidada, obsesionada por aparentar todavía lo que había sido y dejó de ser, creyente a pie juntillas de que el mañana aún es el ayer. Doña Águeda y don Cecilio, desdeñosos de Quevedo, discípulos aventajados de Fausto y Dorian Gray, creían firmemente en la esencia de su arte y en la eterna juventud, aspiraban a la inmortalidad en vida y sólo en la apariencia tenían fe. Quien los veía por primera vez no podía sospechar que se trataba de una pareja de ancianitos ya octogenarios; quien los veía más de una vez, se desesperaba ante tan patética ficción. Y para acabar con ellos, pues creo que he dado completa descripción, es necesario añadir que, poco ha, doña Águeda falleció. A pesar de sus constantes cuidados, afeites y mejunjes, la muerte ha terminado por vencer a quien durante tanto tiempo se empeñó en parecer quien ya no era quien fue. Sic transit Gloria Swanson. III. “LA BRUJA” En el primero izquierda vivía la Bruja, perdón, doña Celeste. Era doña Celeste una mujer madura, una de las originarias inquilinas que, en un momento de debilidad mental, nuestros mayores creyeron apacible y honrada. Porque, como bien pronto se pudo comprobar, doña Celeste era la maldad hecha carne: hablaba mal de todos, era rencorosa y vengativa, siempre tramaba algo contra los demás y difundía bulos que acabaron con más de un matrimonio. Ningún vecino salía a la calle cuando estaba ella en el balcón, no fuera a ser que difundiera en voz alta un bulo o le tirara una maceta en la cabeza. Infundía el pánico en todos cuantos la trataban. Pero lo peor no era esto. No. Doña Celeste había enviudado pronto de su marido, un apocado abogado llamado don Fructuoso. Y contaban las malas lenguas (malas, pero nunca tanto como la de doña Celeste) que el marido no murió de muerte natural (como certificó la autopsia) sino que ella lo mató. Y es más, algunas de esas malas lenguas aseguraban que ella lo apuñaló, lo cual constituía evidencia palmaria de la maldad de doña Celeste (pues se sabe que, entre las mujeres, el modus operandi habitual consiste en suministrar  veneno) y, de paso, levantó leve sospecha de la ineptitud del forense. Pero, por lo visto, nadie se molestó en dar crédito a esos rumores y ella evitó cualquier roce con la justicia. Además, doña Celeste, siempre muy hábil y astuta, trató de mejorar su imagen mostrándose como una mujer bondadosa y apesadumbrada durante el tiempo en que duró el luto. Tenía, además, un niño pequeño al que alimentar, lo cual le sirvió para redondear su ficción como madre coraje, viuda y abandonada. Pero cuando pasó el luto, ella volvió a las andadas. Y el niño se hizo grande y demostró tener los mismos genes de su madre (pues del padre parecía no haber heredado ninguno): era sanguíneo, violento, irritable y visceral (si que es que el significado de todos esos adjetivos se puede sumar); amenazaba a los vecinos, amenazaba a los tenderos para que perdonaran las deudas contraídas por su madre, nos amenazaba a nosotros. Y la madre, peor aún: nos tenía ojeriza, a pesar de ser bizca (razón por la cual los vecinos decían que tenía una mirada torva); nos azuzaba a su hijo a la primera de cambio, sobre todo cuando no teníamos cambio de la difunta peseta del pico del alquiler que, por supuesto, nunca nos perdonaba. Y todavía seguimos así con la dichosa señora y su hijo: a veces, en estado de guerra fría; a veces en estado de guerra caliente (aunque esperemos que nunca desentierren el puñal). Tan sólo en contadas ocasiones nos conceden la tregua y nos hablan como personas civilizadas, pero aun en esas ocasiones nos estremecemos de la sibilina maldad de doña Celeste: de hecho, hace poco, en verano, vimos en su puerta un crespón negro; sin que fuera día de cobro de alquiler, nos atrevimos a llamar (aunque casi era un suicidio hacerlo) y a interesarnos por tan luctuosa situación; doña Celeste abrió y, de manera distendida y casi alegre, nos explicó que ponía ese crespón porque así los ladrones pensarían que en esa casa estaban de luto y entonces, movidos por la compasión, se abstendrían de entrar a robar, para no acrecentar más la pena de los que allí aún vivían."""})
                
                
                total_tokens = num_tokens_from_messages(messages=messages)
                # print(total_tokens)
                if total_tokens < LIMIT_TOKENS:
                    response = openai.ChatCompletion.create(
                        model=MODEL,
                        messages=messages,
                        max_tokens=MAX_TOKENS,
                        temperature=TEMPERATURE,
                    )
                    
                    print(response)

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
            print(exception_data)
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
    logout(request)
    return JsonResponse({'message': 'Adiós', 'isLogout': True}, status=200)

def num_tokens_from_messages(messages):
    model = 'gpt-3.5-turbo'
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens_per_message = 4
    # encodig_per_message = []
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            # encodig_per_message.append({
            #     encoding: encoding.encode(value),
            #     len: len(encoding.encode(value))
            # })
            num_tokens += len(encoding.encode(value)) 

            # if key == 'name':  # si hay un nombre, se omite el rol
            #     num_tokens += -1  # el rol siempre es requerido y siempre 1 token
    num_tokens += 2
    return num_tokens