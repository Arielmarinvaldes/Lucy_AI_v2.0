
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets

import sys
import datetime
from chat import speaks
from login.gui_Admin import Ui_AdminPanel_4
from login.gui_register import Ui_Register
from conection.conexion import establecer_conexion
from voices.voices import talk
from security.protect import (verificar_hash,
                              verificar_len_password, 
                              verificar_capital_password, 
                              verificar_digit_password, 
                              verificar_illegal_character_password, 
                              verificar_space_password, 
                              verificar_exist_password_login,
                              )


class Estructured(QMainWindow):
    login_successful = pyqtSignal()
    def __init__(self) :
        super(Estructured, self).__init__()
        loadUi('login\\interfazModel\\Login.ui', self)
        
        # Controladores
        self.btn_login.clicked.connect(self.login)
        self.btn_signUp.clicked.connect(self.register)
        
        self.password_entry_login.returnPressed.connect(self.btn_login.click)
        self.password_entry_login.setEchoMode(QLineEdit.Password)
        self.checkBox_login.stateChanged.connect(self.toggle_password_visibility)
        
        
        # Ajustes
        self.setWindowTitle("Login")
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setFixedSize(300, 435)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        
        # Crear un temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_next_letter)
        self.timer.start(100)  # Cambia el intervalo según lo desees

        self.messages = ["Hola soy LUCY y no encuentro",
                        "tu rostro en mi base de datos",
                        "Por favor proporcione sus", 
                        "credenciales para iniciar."]
        
        self.current_message_index = 0
        self.current_letter_index = 0
        
        self.COLUMN_WIDTH = 171      

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password_entry_login.setEchoMode(QLineEdit.Normal)  # Mostrar contraseña
        else:
            self.password_entry_login.setEchoMode(QLineEdit.Password)  # Mostrar asteriscos
            
            
    def add_next_letter(self):
        if self.current_message_index < len(self.messages):
            current_message = self.messages[self.current_message_index]

            if self.current_letter_index < len(current_message):
                current_letters = current_message[:self.current_letter_index + 1]
                # Verificar si el elemento ya existe
                if self.current_message_index < self.listWidget_login.count():
                    item = self.listWidget_login.item(self.current_message_index)
                    item.setText(current_letters)
                else:
                    # Si no existe, crear un nuevo elemento
                    self.listWidget_login.addItem(current_letters)
                self.current_letter_index += 1

                # Si se excede el ancho de columna, pasar a la siguiente fila
                if self.current_letter_index == len(current_message):
                    self.current_letter_index = 0
                    self.current_message_index += 1
        else:
            self.timer.stop()

                
    def login(self):
        user = self.user_name_entry_login.text()
        password = self.password_entry_login.text()
        if not user or not password:
            QMessageBox.critical(self, "Error", "Por favor, introduce un nombre de usuario y una contraseña.")
            return

        if verificar_exist_password_login(user, password) and \
           verificar_len_password(password) and \
           verificar_space_password(password) and \
           verificar_capital_password(password) and \
           verificar_digit_password(password) and \
           verificar_illegal_character_password(password):
            pass
        # Conexión a la base de datos SQLite
        conn = establecer_conexion()
        cursor = conn.cursor()

        try:
            # Busca el usuario en la base de datos
            cursor.execute('SELECT hashed_password, salt FROM usuarios WHERE User=?', (user,))
            result = cursor.fetchone()

            if result:
                if user == "Admin":
                    talk("Bienvenidos al modo Administrador")
                    self.close()
                    action = 'Login_Admin'
                    logs = self.admin(user, action)
                else:
                    hashed_password, salt = result
                    if verificar_hash(password, hashed_password, salt):
                        talk(f"Bienvenido, {user}!")
                        print(f"Bienvenido, {user}!")
                        self.close()
                        action = 'Login_User'
                        res = self.admin(user, action)
                        
                        speaks.run(True)
                    else:
                        QMessageBox.critical(self, "Error", "Contraseña incorrecta. Acceso denegado.")
            else:
                # talk("Usuario no encontrado. Acceso denegado.")
                QMessageBox.critical(self, "Error", "Usuario no encontrado. Acceso denegado.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al autenticar usuario: {e}")
        finally:
            conn.close()


    def register(self):
        self.ventana=QtWidgets.QMainWindow()
        self.uir=Ui_Register()
        self.uir.setupUi(self.ventana)
        self.ventana.show()
        
    def admin(self, user, action):
        
        if user == "Admin":
            self.ventana=QtWidgets.QMainWindow()
            self.uia=Ui_AdminPanel_4()
            self.uia.setupUi(self.ventana)
            self.ventana.show()
        
            self.uia.log(user, action)
            self.uia.show_logs()
            
        elif user != "Admin":
            self.uia.log(user, action)
            self.uia.show_logs()
    def res():
        pass
            
def init():
    app = QApplication(sys.argv)
    login_window = Estructured()
    login_window.show()
    sys.exit(app.exec_())