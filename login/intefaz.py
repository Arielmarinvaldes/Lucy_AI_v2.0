import re
import os
import hashlib
import time
import tkinter as tk
import sqlite3
from voices.voices import talk
from camara.face_trainer import trainer
from camara.face_capture import capture_video
from camara.face_capture import run as runcapture
import listen as litn

def verificar_contraseña(password):
    if len(password) < 6:
        talk("Error: La contraseña debe tener al menos 6 caracteres.")
        return False
    
    # Verifica si la contraseña consiste solo en espacios o puntos
    if password.isspace() or password == '.' * len(password):
        talk("Error: La contraseña no puede consistir solo en espacios o puntos.")
        return False
    
    # Verifica si la contraseña contiene al menos una mayúscula y al menos un número
    if not re.search(r"[A-Z]", password):
        talk("Error: La contraseña debe contener al menos una letra mayúscula.")
        return False
    
    if not re.search(r"\d", password):
        talk("Error: La contraseña debe contener al menos un número.")
        return False
    
    # Verifica si la contraseña contiene caracteres no permitidos
    caracteres_no_permitidos = r"/()?¿&%$#@!¡¨{}[]+\-^`"
    if re.search(f"[{re.escape(caracteres_no_permitidos)}]", password):
        talk("  La contraseña contiene caracteres no permitidos.")
        return False

    # La contraseña pasa todas las verificaciones
    return True

# Función para hashear una contraseña y generar un salt
def hash_password(password):
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return hashed_password, salt

# Función para verificar si la contraseña ingresada coincide con la almacenada como hash
def verificar_hash(password, hashed_password, salt):
    new_hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return new_hashed_password == hashed_password

def abrir_registro_usuario():
    # Crear la interfaz gráfica
    root_registro = tk.Tk()
    root_registro.title("Registro de Usuarios")
    root_registro.geometry("200x220")
    root_registro.resizable(0, 0)
    root_registro.configure(bg='#FF9EA0')
    root_registro.eval(f'tk::PlaceWindow {str(root_registro)} center')


    regist_nombre = tk.Label(root_registro, text="Nombre:", bg="#FF9EA0")
    regist_entry_nombre = tk.Entry(root_registro)

    regist_apellido = tk.Label(root_registro, text="Apellido:",bg="#FF9EA0")
    regist_entry_apellido = tk.Entry(root_registro)
    regist_user = tk.Label(root_registro, text="User:",bg="#FF9EA0")
    regist_entry_user = tk.Entry(root_registro)

    regist_password = tk.Label(root_registro, text="Password:",bg="#FF9EA0")
    regist_entry_password = tk.Entry(root_registro, show="*")  # Configurar show="*" para ocultar los caracteres
    
    button_registrar = tk.Button(root_registro, text="Registrar Usuario", command=lambda: registrar_usuario(
        root_registro, regist_entry_nombre.get(), regist_entry_apellido.get(), regist_entry_user.get(), regist_entry_password.get()
    ))

    regist_nombre.pack()
    regist_entry_nombre.pack()
    regist_apellido.pack()
    regist_entry_apellido.pack()
    regist_user.pack()
    regist_entry_user.pack()
    regist_password.pack()
    regist_entry_password.pack()
    button_registrar.place(x=50, y=180)
    root_registro.mainloop()
    


# Función para registrar usuarios
def registrar_usuario(root, nombre, apellido, user, password):
    
    if not user or not password or not nombre or not apellido:
        talk("Error Por favor complete los campos vacíos.")
        return
    hashed_password, salt = hash_password(password)
    if verificar_contraseña(password):
        pass
    else:
        talk("Contraseña no válida. Acceso denegado.")
        return
    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('db\\users.db')
    cursor = conn.cursor()
    # Verifica si la tabla usuarios existe, si no, créala
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT,
            Apellido TEXT,
            User TEXT,
            hashed_password TEXT,
            salt TEXT
        )
    ''')
    # Inserta los datos del usuario en la base de datos
    cursor.execute('INSERT INTO usuarios (Nombre, Apellido, User, hashed_password, salt) VALUES (?, ?, ?, ?, ?)', (nombre, apellido, user, hashed_password, salt))
    # Guarda los cambios y cierra la conexión
    conn.commit()
    conn.close()
    # Llama a la función para capturar el video de la reconocimiento
    capture_video()
    # cerrar la ventana despues de terminar el reconocimiento
    root.destroy()
    # Llama a la función para capturar el rostro del video para el reconocimiento del usuario nuevo
    runcapture(nombre)
    # Espera un tiempo antes de eliminar el video temporal
    time.sleep(1)
    # Ruta del archivo de video con el número de seguimiento
    video_filename = f'camara\\video_usuario_1.avi'
    # Elimina el video temporal
    os.remove(video_filename)
    # Entrenando el modelo de reconocimiento
    trainer()
    talk("Ya puede iniciar seción")


# Función para iniciar sesión
def login(user_entry, password_entry, root, check):
    user = user_entry
    password = password_entry

    if not user or not password:
        talk("Error. Por favor complete ambos campos para iniciar seción.")
        return

    if verificar_contraseña(password):
        pass

    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('db\\users.db')
    cursor = conn.cursor()

    # Verifica si la tabla usuarios existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT,
            Apellido TEXT,
            User TEXT,
            hashed_password TEXT,
            salt TEXT
        )
    ''')

    # Busca el usuario en la base de datos
    cursor.execute('SELECT hashed_password, salt FROM usuarios WHERE User=?', (user,))
    result = cursor.fetchone()

    conn.close()

    if result:
        hashed_password, salt = result
        if verificar_hash(password, hashed_password, salt):
            # La contraseña es válida, puedes permitir el inicio de sesión
            talk(f"Bienvenido, {user}!")
            print(f"Bienvenido, {user}!")
            root.destroy()
            litn.main(check)
        else:
            talk("Contraseña incorrecta. Acceso denegado.")
    else:
        talk("Usuario no encontrado. Acceso denegado.")


def gui():
    # Crear la interfaz principal
    root = tk.Tk()
    root.title("LOGIN")
    root.geometry("200x250")
    root.resizable(0, 0)
    root.configure(bg='#FF9EA0')
    root.eval(f'tk::PlaceWindow {str(root)} center')
    # Evita que la ventana se pueda cerrar con el botón de cierre
    # root.overrideredirect(1)

    inicio_user = tk.Label(root, text="User:", bg="#FF9EA0")
    entry_user = tk.Entry(root)

    inicio_password = tk.Label(root, text="Password:",bg="#FF9EA0")
    entry_password = tk.Entry(root, show="*")

    # Boton Iniciar el Asistente
    boton_login = tk.Button(root, text="Login", command=lambda: login(entry_user.get(), entry_password.get(), root, var.get()))

    # Botón para abrir la interfaz de registro de usuarios
    button_abrir_registro = tk.Button(root, text="Registrar Usuario", command=abrir_registro_usuario)
    
    var = tk.BooleanVar()
    var.set(False)
    radio_button = tk.Label(root, text="Modo de Inicio",bg="#FF9EA0")
    check_button_manual = tk.Radiobutton(root, text="manual",bg="#FF9EA0", variable=var, value=False)
    check_button_auto = tk.Radiobutton(root, text="auto",bg="#FF9EA0", variable=var, value=True)
    
    inicio_user.pack()
    entry_user.pack()
    inicio_password.pack()
    entry_password.pack()
    boton_login.place(x=80, y=100)
    button_abrir_registro.place(x=50, y=150)
    radio_button.place(x=60, y=190)
    check_button_manual.place(x=30, y=220 )
    check_button_auto.place(x=120, y=220 )

    return root.mainloop()
