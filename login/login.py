from voices.voices import talk
import re
import os
import time
import tkinter as tk
import sqlite3
from camara.face_capture import capture_video
from camara.face_trainer import trainer
from camara.face_capture import run as runcapture


def verificar_contraseña(password):
    # Verifica longitud mínima de la contraseña
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


# Función para alternar la visibilidad de la contraseña
def toggle_password_visibility():
    if show_password.get():
        regist_entry_password.config(show="")
    else:
        regist_entry_password.config(show="*")

def presionar_enter(event):
    login()

def abrir_registro_usuario():
    global root_registro, regist_entry_password, show_password,regist_entry_nombre,regist_entry_apellido,regist_entry_user,regist_entry_password

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
    show_password_checkbox.place(x=170, y=140)
    button_registrar.place(x=50, y=180)
    root_registro.mainloop()


# Función para registrar usuarios
def registrar_usuario():
    nombre = regist_entry_nombre.get().capitalize()
    apellido = regist_entry_apellido.get().capitalize()
    user = regist_entry_user.get()
    password = regist_entry_password.get()

    if not user or not password or not nombre or not apellido:
        talk("Error Por favor complete los campos vacíos.")
        return

    if verificar_contraseña(password):
        pass
    else:
        talk("Contraseña no válida. Acceso denegado.")
        return

    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('db\\usuarios.db')
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

    # Inserta los datos del usuario en la base de datos
    cursor.execute('INSERT INTO usuarios (Nombre, Apellido, User, Password) VALUES (?, ?, ?, ?)', (nombre, apellido, user, password))

    # Guarda los cambios y cierra la conexión
    conn.commit()
    conn.close()

    # Llama a la función para capturar el video de la reconocimiento
    capture_video()

    # cerrar la ventana despues de terminar el reconocimiento
    root_registro.destroy()

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
def login():
    user = entry_user.get()
    password = entry_password.get()

    
    if not user or not password:
        talk("Error,  Por favor complete ambos campos para iniciar seción.")
        return

    if verificar_contraseña(password):
        pass

    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('db\\usuarios.db')
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
        talk(f"Bienvenido {nombre}")
        print(f"Bienvenido, {nombre}")
        root.destroy()
    else:
        # Si no se encontró un usuario, muestra un mensaje de error
        talk("Error,  Usuario o contraseña incorrectos")
    return 

def main_root():
    global root, entry_user, entry_password
    # Crear la interfaz principal
    root = tk.Tk()
    root.title("iniciar sesion")
    root.geometry("200x200")
    root.resizable(0, 0)
    root.configure(bg='#FF9EA0')
    root.eval(f'tk::PlaceWindow {str(root)} center')
    # Evita que la ventana se pueda cerrar con el botón de cierre
    root.overrideredirect(1)
    # root.protocol("WM_DELETE_WINDOW")

    inicio_user = tk.Label(root, text="User:", bg="#FF9EA0")
    entry_user = tk.Entry(root)

    inicio_password = tk.Label(root, text="Password:",bg="#FF9EA0")
    entry_password = tk.Entry(root, show="*")

    # Boton Iniciar el Asistente
    boton_login = tk.Button(root, text="Ingresar", command=login)

    # Botón para abrir la interfaz de registro de usuarios
    button_abrir_registro = tk.Button(root, text="Registrar Usuario", command=abrir_registro_usuario)
    root.bind('<Return>', presionar_enter)

    inicio_user.pack()
    entry_user.pack()
    inicio_password.pack()
    entry_password.pack()
    boton_login.place(x=75, y=100)
    button_abrir_registro.place(x=50, y=150)

    return root.mainloop()

