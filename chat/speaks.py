import logging
from search.search import busca as srh
from search.search import reproduce as rep
from search.search import chiste
from voices.voices import talk as talk
from voices.voices import spanish_voice as spanish
from voices.voices import english_voice as english
from camara.lucy_cam import camara as cam
# from camara.face_recognizer import reconocimiento as fr
from chat.chat_wasapp import envia_mensaje as send
from system.funtion_sys import thread_alarma
from system.funtion_sys import escribe
from system.funtion_sys import clima
from system.funtion_sys import fecha
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chat import chat_bot as db
from motor.motor import listen, recognize_audio


LOG_FILE = 'chat\\chatbot_log.log'
CHATBOT_NAME = 'lucy'

# Configuración de logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# diccionario con palabras claves
key_words = {
    "reproduce": rep,
    "busca,": srh,
    "busca": srh,
    "buzca,": srh,
    "alarma": thread_alarma,
    "cámara": cam,
    "cámara.": cam,
    # "reconocimiento": fr,
    "escribe": escribe,
    "clima.": clima,
    "clima": clima,
    "tiempo": clima,
    "qué": fecha,
    "chiste": chiste,
    "voz1": english,
    "vos1": english,
    "vos1.": english,
    "voz24": spanish,
    "mensaje": send,
}


def run(modo_automatico=True):
    # Inicializa el chatbot y el entrenador
    chat = ChatBot(CHATBOT_NAME)
    trainer = ListTrainer(chat)

    # Entrena el chatbot con preguntas y respuestas de la base de datos
    training_set = [tupla[0] for tupla in db.get_questionanswers()]  # Obtene solo las preguntas
    trainer.train(training_set)

    # Entrena el chatbot con datos del corpus en español
    trainer.train("chatterbot.corpus.spanish")

    while True:
        try:
            # Obtener la entrada del usuario
            if modo_automatico:
                # Modo automático (audio)
                audio_path = listen()
                user_input = recognize_audio(audio_path).lower().strip()
            else:
                # Modo manual (entrada de texto)
                user_input = input("Tú: ").lower().strip()

            # Analizar la entrada del usuario
            command, *word = user_input.split()
            word = " ".join(word)

            # Verifica los comandos especiales
            if command in key_words:
                key_words[command](word)
            
            elif 'termina.' in user_input:
                talk("Hasta luego")
                break

            else:
                # Respuesta del chatbot
                print("Tú:", user_input)
                answer = chat.get_response(user_input)
                print("Lucy:", answer)
                talk(answer)

        except UnboundLocalError:
            talk("No entendí. Repite")
        except KeyError as e:
            print("Parámetro de entrada incorrecto", e)
        except Exception as e:
            logging.error(f"Lo siento, hubo un error: {str(e)}")
