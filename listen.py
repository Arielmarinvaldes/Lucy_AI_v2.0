import logging
from search.search import busca as srh
from search.search import reproduce as rep
from search.search import chiste
from voices.voices import talk as talk
from voices.voices import spanish_voice as spanish
from voices.voices import english_voice as english
from camara.lucy_cam import camara as cam
from camara.face_recognizer import reconocimiento as fr
from system.funtion_sys import thread_alarma
from chat.chat_wasapp import envia_mensaje as send
from system.funtion_sys import escribe
from system.funtion_sys import clima
from system.funtion_sys import fecha
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chat import database as db
from motor.motor import listen, recognize_audio
import login.intefaz as intfz


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
    "reconocimiento": fr,
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


def main(modo_automatico=True):
    chat = ChatBot(CHATBOT_NAME)
    trainer = ListTrainer(chat)
    
    training_set = []
    for tupla in db.get_questionanswers():
        training_set.append(tupla[0])
        training_set.append(tupla[1])
    trainer.train(training_set)
    trainer.train("chatterbot.corpus.spanish")

    while True:
        try:
            # Voice mode
            if modo_automatico:
                audio_path = listen()
                rec = recognize_audio(audio_path).lower().strip().split(" ")
                command = rec[0]
                print(f"Command 1: '{command}', Input: {rec}")
                word = ""
                if len(rec) > 1:
                    word = " ".join(rec[1:])
            else:
                # Manual mode
                user_input = input("Tú: ")
                command = user_input.split(" ")[0]
                print(f"Command 2: '{command}', Input: {user_input}")
                word = " ".join(user_input.split(" ")[1:])

            if command in key_words:
                key_words[command](word)
            
            elif 'termina.' in (rec if modo_automatico else user_input):
                talk("Hasta luego")
                break

            else:
                input_text = " ".join(rec) if modo_automatico else user_input
                print("Tú: ", input_text)
                answer = chat.get_response(input_text)
                print("Lucy: ", answer)
                talk(answer)

        except UnboundLocalError:
            talk("No entendí. Repite")
        except KeyError as e :
            print("Paámetro de entrada incorrecto", e)
        except Exception as e:
            logging.error(f"Lo siento, hubo un error{str(e)}")


if __name__ == '__main__':
    intfz.gui()