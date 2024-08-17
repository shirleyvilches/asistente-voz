import pyttsx3
import speech_recognition as sr
import pyaudio
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# Transformar voz en texto
def reconocer_voz_witai():
    # Crear un objeto Recognizer
    reconocedor = sr.Recognizer()

    # Utilizar el micrófono como fuente de audio
    with sr.Microphone() as fuente:
        print("Habla algo:")
        # Ajustar niveles de ruido automáticamente
        reconocedor.adjust_for_ambient_noise(fuente)

        try:
            # Escuchar y reconocer la voz utilizando el servicio de Wit.ai
            audio = reconocedor.listen(fuente, timeout=5)

            # Configurar la clave de API de Wit.ai
            witai_key = "LJ6LZRBPRQGG6T2VVRFUTCY3F3LH5SFT"

            # Utilizar el reconocedor de Wit.ai para convertir el audio en texto
            texto = reconocedor.recognize_wit(audio, key=witai_key).lower()
            print(f"Has dicho: {texto}")
            return texto
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
        except sr.RequestError as e:
            print(f"Error al realizar la solicitud a Wit.ai: {e}")


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    #encender el motor de pyttsx3
    engine  = pyttsx3.init()

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


#elegir voz
"""engine = pyttsx3.init()
for voz in engine.getProperty('voices'):
    print(voz)"""

def pedir_dia():
    #crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    #crear dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)

    #dias de semana
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}
    #decir el dia de la semana
    hablar(f'Hoy es{calendario[dia_semana]}')


def pedir_hora():
    # crear variable con datos de hoy
    hora = datetime.datetime.now()
    formatted_time = hora.strftime("%H:%M")
    print(formatted_time)

    # decir la hora
    hablar(f'La hora es {formatted_time}')


def saludo_inicial():
    #determinar momento del dia
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour >= 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buenos días"
    else:
        momento = "Buenas tardes"

    #decir saludo
    hablar(f"{momento} mi mago favorito! ¿Qué desea hacer hoy?")


#Fundion central del asistente
def pedir_cosas():
    #activar saludo inicial
    saludo_inicial()

    #variable de corte
    comenzar = True

    while comenzar:
       #activar micro y guardar el pedido en un string
        pedido = reconocer_voz_witai()

        if 'abrir youtube' in pedido:
           hablar('Con gusto, estoy abriendo youtube')
           webbrowser.open("https://www.youtube.com/")
           continue
        elif 'abrir netflix' in pedido:
            hablar('Con gusto, estoy abriendo netflix')
            webbrowser.open("https://www.netflix.com/browse")
            continue
        elif 'que dia es hoy' in pedido:
            pedir_dia()
            continue
        elif 'que hora es' in pedido:
            pedir_hora()
            continue
        elif 'buscar en wikipedia' in pedido:
            hablar('Buscando en wikipedia')
            pedido = pedido.replace('wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("Wikipedia dice lo siguiente")
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar("Estoy en eso")
            pedido = pedido.replace("busca en internet", '')
            pywhatkit.search(pedido)
            hablar("Esto he encontrado")
            continue
        elif 'reproducir' in pedido:
            hablar("Excelente idea")
            pywhatkit.playonyt(pedido)
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip
            cartera = {'apple':'APPL',
                       'google':'GOOGL',
                       'amazon':'AMZN'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar("Perdón, pero no la he encontrado")
                continue
        elif 'adios' in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            break

pedir_cosas()


