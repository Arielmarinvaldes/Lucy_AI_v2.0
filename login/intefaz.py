from chat import speaks
import tkinter as tk
from tkinter import messagebox
import sqlite3
import time
import os
from conection.conexion import establecer_conexion
from voices.voices import talk
from camara.face_trainer import trainer
from camara.face_capture import capture_video
from camara.face_capture import run as runcapture
from security.protect import (hash_password, 
                              verificar_len_password, 
                              verificar_capital_password, 
                              verificar_digit_password, 
                              verificar_hash, 
                              verificar_illegal_character_password, 
                              verificar_space_password, 
                              verificar_exist_password_regist,
                              verificar_exist_password_login
                              ) 

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
    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('db\\users.db')
    cursor = conn.cursor()

    
    hashed_password, salt = hash_password(password)
    if verificar_len_password(password) and \
       verificar_space_password(password) and \
       verificar_capital_password(password) and \
       verificar_digit_password(password) and \
       verificar_exist_password_regist(user, password, nombre, apellido) and \
       verificar_illegal_character_password(password):
        pass
    else:
        talk("Contraseña no válida. Acceso denegado.")
        return
    
    # Verifica si la tabla usuarios existe, si no, la créara
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

    if verificar_exist_password_login(user, password) and \
       verificar_len_password(password) and \
       verificar_space_password(password) and \
       verificar_capital_password(password) and \
       verificar_digit_password(password) and \
       verificar_illegal_character_password(password):
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
        if user == "Admin":
            talk("Bienvenidos al modo Administrador")
            # Admin_gui()
        else:  
            hashed_password, salt = result
            if verificar_hash(password, hashed_password, salt):
                # Si la contraseña es válida, puedes permitir el inicio de sesión
                talk(f"Bienvenido, {user}!")
                print(f"Bienvenido, {user}!")
                root.destroy()
                speaks.run(check)
            else:
                talk("Contraseña incorrecta. Acceso denegado.")
    else:
        talk("Usuario no encontrado. Acceso denegado.")
        
        
class Admin_gui():
    def __init__(self):
        # Crear la interfaz gráfica
        self.root = tk.Tk()
        self.root.title("Admin Panel")
        self.root.geometry("500x500")
        self.root.resizable(0, 0)
        self.root.configure(bg='#FF9EA0')
        self.root.eval(f'tk::PlaceWindow {str(self.root)} center')

        # Botones CRUD
        button_positions = {'Crear User': 30, 'Update User': 70, 'Delete User': 110, 'Get User': 150}
        self.buttons = {}
                
        button_colors = ["#FFF88E", "#27BAD6", "#FF2929", "#82E97D"] 
        for (text, y_position), color in zip(button_positions.items(), button_colors):
            button = tk.Button(self.root, text=text, width=15, command=lambda t=text: self.button_clicked(t), bg=color)
            button.place(x=360, y=y_position)
            self.buttons[text] = button
            
        # Boton Delete All Users
        drop_all_users = tk.Button(self.root, text="Delete DB",width=15, bg="#323232" , fg="#FFFFFF")
        drop_all_users.place(x=360, y=350)

        # Cajas de texto para entrada de datos
        self.etiqueta_id = tk.Label(self.root, text="ID:", bg='#FF9EA0')
        self.etiqueta_id.place(x=5, y=40)
        self.entradas_id = tk.Entry(self.root, width=3)
        self.entradas_id.place(x=25, y=40)
        
        self.etiqueta_nombre = tk.Label(self.root, text="Name", bg='#FF9EA0')
        self.etiqueta_nombre.place(x=60, y=20)
        self.entradas_nombre = tk.Entry(self.root, width=12)
        self.entradas_nombre.place(x=60, y=40)
        
        
        self.etiqueta_apellido = tk.Label(self.root, text="Last Name", bg='#FF9EA0')
        self.etiqueta_apellido.place(x=40, y=70)
        self.entradas_apellido = tk.Entry(self.root)
        self.entradas_apellido.place(x=10, y=90)
        
        self.etiqueta_user = tk.Label(self.root, text="User", bg='#FF9EA0')
        self.etiqueta_user.place(x=60, y=120)
        self.entradas_user = tk.Entry(self.root)
        self.entradas_user.place(x=10, y=140)
        
        self.etiqueta_passw = tk.Label(self.root, text="Password", bg='#FF9EA0')
        self.etiqueta_passw.place(x=45, y=170)
        self.entradas_passw = tk.Entry(self.root)
        self.entradas_passw.place(x=10, y=190)
        
        # Variable para limpiar los Entrys
        self.entry_widgets_to_clear = [self.entradas_nombre, self.entradas_apellido, self.entradas_user, self.entradas_passw, self.entradas_id]
        # Frame para mostrar los datos
        self.data_frame = tk.Frame(self.root, width=200, height=200, bg='white', bd=2, relief='solid')
        self.data_frame.place(x=140, y=30)
        self.data_frame.pack_propagate(False)

        # Encabezados
        headers = ['ID', 'Nombre', 'Apellido', 'User']
        for col, header in enumerate(headers):
            tk.Label(self.data_frame, text=header, bg='lightgray').grid(row=0, column=col, padx=5, pady=5)

        self.root.mainloop()

    def button_clicked(self, button_text):
        if button_text == 'Crear User':
            self.create_user_function(self.entradas_nombre.get(), self.entradas_apellido.get(), self.entradas_user.get(), self.entradas_passw.get())
        elif button_text == 'Update User':
            self.update_user_function(self.entradas_id.get(),self.entradas_nombre.get(), self.entradas_apellido.get(), self.entradas_user.get(), self.entradas_passw.get())
        elif button_text == 'Delete User':
            self.delete_user_function(self.entradas_id.get())
        elif button_text == 'Get User':
            self.get_user_function()

    def create_user_function(self, name, last_name, user_name, password):
        hashed_password, salt = hash_password(password)
        if  verificar_len_password(password) and \
            verificar_space_password(password) and \
            verificar_capital_password(password) and \
            verificar_digit_password(password) and \
            verificar_exist_password_regist(user_name, password, name, last_name) and \
            verificar_illegal_character_password(password):
            pass
        else:
            talk("Contraseña no válida. Acceso denegado.")
            return
        conn = establecer_conexion()
        try:
            # Obtener datos de las cajas de texto
            nombre = name
            apellido = last_name
            user = user_name

            # Insertar datos en la base de datos
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (Nombre, Apellido, User, hashed_password, salt) VALUES (?, ?, ?, ?, ?)",
                           (nombre, apellido, user, hashed_password, salt))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario creado con éxito")
            
            for entry_widget in self.entry_widgets_to_clear:
                entry_widget.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear usuario: {e}")

        finally:
            conn.close()

    def update_user_function(self, user_id, name, last_name, user, password):
        if not user_id:
            messagebox.showerror("Error", "Por favor, proporciona un ID de usuario.")
            return
        
        hashed_password, salt = hash_password(password)
        if  verificar_len_password(password) and \
            verificar_space_password(password) and \
            verificar_capital_password(password) and \
            verificar_digit_password(password) and \
            verificar_exist_password_regist(user, password, name, last_name) and \
            verificar_illegal_character_password(password):
            pass
        else:
            # talk("Contraseña no válida. Acceso denegado.")
            return
        
        conn = establecer_conexion()
        
        try:
            # Actualiza el usuario en la base de datos
            cursor = conn.cursor()
            cursor.execute("UPDATE Usuarios SET Nombre=?, Apellido=?, User=?, hashed_password=?, salt=? WHERE id=?",
                           (name, last_name, user, hashed_password, salt, user_id))
            conn.commit()
            messagebox.showinfo("Éxito", f"Usuario con ID {user_id} actualizado con éxito")
            
            for entry_widget in self.entry_widgets_to_clear:
                entry_widget.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar usuario: {e}")

        finally:
            conn.close()
            
            
    def delete_user_function(self, user_id):
        if not user_id:
            messagebox.showerror("Error", "Por favor, proporciona un ID de usuario.")
            return
        conn = establecer_conexion()
        try:
            # Elimina el usuario de la base de datos
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id=?", (user_id,))
            conn.commit()
            messagebox.showinfo("Éxito", f"Usuario con ID {user_id} eliminado con éxito")
            
            for entry_widget in self.entry_widgets_to_clear:
                entry_widget.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar usuario: {e}")

        finally:
            conn.close()
        
    def get_user_function(self):
        conn = establecer_conexion()
        try:
            # Obtener datos de la base de datos
            cursor = conn.cursor()
            cursor.execute("SELECT id, Nombre, Apellido, User FROM usuarios")
            users = cursor.fetchall()

            if not users:
                messagebox.showinfo("Información", "No hay información de usuarios disponible.")
            else:
                # Mostrar datos en el Frame
                self.mostrar_datos(users)

        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener usuarios: {e}")

        finally:
            conn.close()
    
    def delete_db_function(self):
        if not confirmacion_db_borrada:
            messagebox.showinfo("Seguro que desea borrar la base de datos")
            confirmacion_db_borrada = True
            return
        
        # ¡WARNING!
        # Codigo de eliminacion
        

        talk("Base de datos eliminada con éxito.")
        confirmacion_db_borrada = False
            
    def mostrar_datos(self, data):
        # Limpiar datos anteriores
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        # Mostrar encabezados
        headers = ['ID', 'Nombre', 'Apellido', 'User']
        for col, header in enumerate(headers):
            tk.Label(self.data_frame, text=header, bg='lightgray').grid(row=0, column=col, padx=5, pady=5)

        # Mostrar datos en el Frame
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                tk.Label(self.data_frame, text=value, bg='white').grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)
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
    check_button_manual = tk.Radiobutton(root, text="Manual",bg="#FF9EA0", variable=var, value=False)
    check_button_auto = tk.Radiobutton(root, text="Voz",bg="#FF9EA0", variable=var, value=True)
    
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