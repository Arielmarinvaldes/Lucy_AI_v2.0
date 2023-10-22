import io
import speech_recognition as sr
import whisper
import tempfile
import os
import time
import logging
import nltk
import tkinter as tk
import cv2
import sqlite3

from pydub import AudioSegment
from search.search import busca as srh
from search.search import reproduce as rep
from voices.voices import talk as talk
from camara.lucy_cam import camara as cam
from camara.face_recognizer import reconocimiento as fr
from camara.face_capture import capture_video
from system.funtion_sys import thread_alarma
from chat.chat_wasapp import envia_mensaje as send
from camara.face_capture import run as runcapture

from chatterbot import ChatBot
from chatterbot import preprocessors
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from collections.abc import MutableMapping
from chat import database as db
from chat.chat_wasapp import envia_mensaje
from motor.motor import listen, recognize_audio


# Función para alternar la visibilidad de la contraseña
def toggle_password_visibility():
    if show_password.get():
        regist_entry_password.config(show="")
    else:
        regist_entry_password.config(show="*")


def abrir_registro_usuario():
    global root_registro, regist_entry_password, show_password,regist_entry_nombre,regist_entry_apellido,regist_entry_user,regist_entry_password

    # Crear la interfaz gráfica
    root_registro = tk.Tk()
    root_registro.title("Registro de Usuarios")
    root_registro.geometry("300x320")
    root_registro.resizable(0, 0)
    root_registro.configure(bg='#FF9EA0')

    regist_nombre = tk.Label(root_registro, text="Nombre:", bg="#FF9EA0")
    regist_entry_nombre = tk.Entry(root_registro)

    regist_apellido = tk.Label(root_registro, text="Apellido:",bg="#FF9EA0")
    regist_entry_apellido = tk.Entry(root_registro)

    regist_user = tk.Label(root_registro, text="User:",bg="#FF9EA0")
    regist_entry_user = tk.Entry(root_registro)

    regist_password = tk.Label(root_registro, text="Password:",bg="#FF9EA0")
    regist_entry_password = tk.Entry(root_registro, show="*")  # Configura show="*" para ocultar los caracteres
    show_password = tk.IntVar()
    show_password_checkbox = tk.Checkbutton(root_registro, bg="#FF9EA0", variable=show_password, command=toggle_password_visibility)
    button_registrar = tk.Button(root_registro, text="Registrar Usuario", command=registrar_usuario)

    regist_nombre.pack()
    regist_entry_nombre.pack()
    regist_apellido.pack()
    regist_entry_apellido.pack()
    regist_user.pack()
    regist_entry_user.pack()
    regist_password.pack()
    regist_entry_password.pack()
    show_password_checkbox.place(x=260, y=210)
    button_registrar.place(x=75, y=260)

    root_registro.mainloop()


# Función para registrar usuarios
def registrar_usuario():
    nombre = regist_entry_nombre.get()
    apellido = regist_entry_apellido.get()
    user = regist_entry_user.get()
    password = regist_entry_password.get()

    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Verifica si la tabla usuarios existe, si no, créala
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            user TEXT,
            password TEXT
        )
    ''')

    # Inserta los datos del usuario
    cursor.execute('INSERT INTO usuarios (Nombre, Apellido, User, Password) VALUES (?, ?, ?, ?)', (nombre, apellido, user, password))

    # Guarda los cambios y cierra la conexión
    conn.commit()
    conn.close()

    # Llama a la función para capturar el video
    capture_video()
    root_registro.destroy()
    runcapture()

    # Espera un tiempo antes de eliminar el archivo temporal
    time.sleep(1)

    # Nombre del archivo de video con el número de seguimiento
    video_filename = f'camara\\video_usuario_1.avi'

    # Elimina el archivo temporal
    os.remove(video_filename)


# Función para iniciar sesión
def login():
    user = entry_user.get()
    password = entry_password.get()

    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Verifica si la tabla usuarios existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            user TEXT,
            password TEXT
        )
    ''')

    # Busca el usuario en la base de datos
    cursor.execute('SELECT nombre FROM usuarios WHERE user=? AND password=?', (user, password))
    result = cursor.fetchone()

    conn.close()

    if result:
        # Si se encontró un usuario con el usuario y contraseña proporcionados, muestra un mensaje de bienvenida
        nombre = result[0]
        talk(f"Bienvenido, {nombre}")
        print(f"Bienvenido, {nombre}")
        root.destroy()
    else:
        # Si no se encontró un usuario, muestra un mensaje de error
        talk("Error", "Usuario o contraseña incorrectos")
        print("Error", "Usuario o contraseña incorrectos")


# Crear la interfaz principal
root = tk.Tk()
root.title("iniciar sesion")
root.geometry("300x250")
root.resizable(0, 0)
root.configure(bg='#FF9EA0')

inicio_user = tk.Label(root, text="User:", bg="#FF9EA0")
entry_user = tk.Entry(root)

inicio_password = tk.Label(root, text="Password:",bg="#FF9EA0")
entry_password = tk.Entry(root)

# Boton Iniciar el Asistente
boton_login = tk.Button(root, text="Ingresar", command=login)

# Botón para abrir la interfaz de registro de usuarios
button_abrir_registro = tk.Button(root, text="Registrar Usuario", command=abrir_registro_usuario)

inicio_user.pack()
entry_user.pack()
inicio_password.pack()
entry_password.pack()
boton_login.place(x=110, y=130)
button_abrir_registro.place(x=75, y=190)

root.mainloop()


# Configuración de logging
logging.basicConfig(filename='chatbot_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    "mensaje": envia_mensaje,

}


# Función principal
def main():
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
            audio_path = listen()
            rec = recognize_audio(audio_path).lower().strip().split(" ")
            command = rec[0]
            print(f"Command: '{command}', Input: {rec}")
            word = ""
            if len(rec) > 1:
                word = " ".join(rec[1:])

            if command in key_words:
                key_words[command](word)
            
            elif 'termina.' in rec:
                talk("Hasta luego")
                break

            else:
                rec2 = recognize_audio(audio_path).lower().strip()
                print("Tú: ", rec2)
                answer = chat.get_response(rec2)
                print("Lucy: ", answer)
                talk(answer)

        except UnboundLocalError:
            talk("No entendi. intenta de nuevo")
            continue

        except Exception as e:
            talk("Lo siento, hubo un error")

if __name__ == '__main__':
    main()
