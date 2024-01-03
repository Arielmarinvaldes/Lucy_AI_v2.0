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
from login.login import main_root


# Configuración de logging
logging.basicConfig(filename='chat\\chatbot_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    "voz en ingles": english,
    "vos en ingles": english,
    "vos en ingles.": english,
    "voz en español": spanish,
    "mensaje": send,
}


# Función principal
# def main():
#     chat = ChatBot("lucy")
#     trainer = ListTrainer(chat)
    
#     training_set = []
#     for tupla in db.get_questionanswers():
#         training_set.append(tupla[0])
#         training_set.append(tupla[1])
#     trainer.train(training_set)
#     trainer.train("chatterbot.corpus.spanish")

#     while True:
#         try:
#             audio_path = listen()
#             rec = recognize_audio(audio_path).lower().strip().split(" ")
#             command = rec[0]
#             print(f"Command: '{command}', Input: {rec}")
#             word = ""
#             if len(rec) > 1:
#                 word = " ".join(rec[1:])

#             if command in key_words:
#                 key_words[command](word)
            
#             elif 'termina.' in rec:
#                 talk("Hasta luego")
#                 break

#             else:
#                 rec2 = recognize_audio(audio_path).lower().strip()
#                 print("Tú: ", rec2)
#                 answer = chat.get_response(rec2)
#                 print("Lucy: ", answer)
#                 talk(answer)

#         except UnboundLocalError:
#             talk("No entendi. Repite")
#             continue

#         except Exception as e:
#             talk("Lo siento, hubo un error")


# Esto es una prueba de la funcion (main) para alternar entre el modo por voz y el modo manual.
# Funciona el modo manual perfectamente pero hay errores que corregir.
def main(modo_automatico=True):
    chat = ChatBot("lucy")
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
                print(f"Command: '{command}', Input: {rec}")
                word = ""
                if len(rec) > 1:
                    word = " ".join(rec[1:])
            else:
                # Manual mode
                user_input = input("Tú: ")
                command = user_input.split(" ")[0]
                print(f"Command: '{command}', Input: {user_input}")
                word = " ".join(user_input.split(" ")[1:])

            if command in key_words:
                key_words[command](word)
            
            # El error que presenta esta funcion que cuando cambio a modo voz no me reconoce el audio , pero si yo le digo termina que es para cerrar el programa funciona..
            elif 'termina.' in (rec if modo_automatico else user_input): 
                talk("Hasta luego")
                break

            else:
                input_text = rec if modo_automatico else user_input
                print("Tú: ", input_text)
                answer = chat.get_response(input_text)
                print("Lucy: ", answer)
                talk(answer)

        except UnboundLocalError:
            talk("No entendí. Repite")
            continue

        except Exception:
            talk("Lo siento, hubo un error")

if __name__ == '__main__':
    main_root()
    # Por defecto el modo es automático, se puede cambiar a manual pasando (False) como argumento.
    main(modo_automatico=False)

# if __name__ == '__main__':
#     main_root()
#     main()
