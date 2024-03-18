
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QRadioButton, QLabel
from PyQt5.uic import loadUi


import sys
from chat import speaks
import tkinter as tk
from tkinter import messagebox
import sqlite3
import time
import os
from chat import speaks
from conection.conexion import establecer_conexion
from voices.voices import talk
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




class AdminGUI(QMainWindow):
    def __init__(self):
        super(AdminGUI, self).__init__()
        loadUi('Admin_panel.ui', self)
        
        # Controladores
        self.btn_get.clicked.connect(self.get_user_function)
        self.btn_create.clicked.connect(self.create_user_function)
        self.btn_update.clicked.connect(self.update_user_function)
        self.btn_delete.clicked.connect(self.delete_user_function)
        # self.btn_run.clicked.connect(self.run_function)
        
        self.radio_button_manul.clicked.connect(lambda: speaks.run(False))
        self.radio_button_voice.clicked.connect(lambda: speaks.run(True))
        

    
    def get_user_function(self):
        conn = establecer_conexion()
        try:
            # Obtener datos de la base de datos
            cursor = conn.cursor()
            cursor.execute("SELECT id, Nombre, Apellido, User FROM usuarios")
            users = cursor.fetchall()

            if not users:
                QMessageBox.information(self, "Información", "No hay información de usuarios disponible.")
            else:
                # Limpiar la tabla antes de agregar elementos nuevos
                self.table_widget_principal.clearContents()
                self.table_widget_principal.setRowCount(0)
                
                # Agregar cabeceras
                headers = ["ID", "Nombre", "Apellido", "Usuario"]
                self.table_widget_principal.setColumnCount(len(headers))
                self.table_widget_principal.setHorizontalHeaderLabels(headers)
                
                # Mostrar datos en la tabla
                for row, user in enumerate(users):
                    self.table_widget_principal.insertRow(row)
                    for col, value in enumerate(user):
                        item = QTableWidgetItem(str(value))
                        self.table_widget_principal.setItem(row, col, item)

                # Ocultar la columna de ID
                # self.table_widget_principal.setColumnHidden(0, True)

            # Actualizar la barra de progreso
            self.update_progress_bar()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al obtener usuarios: {e}")

        finally:
            conn.close()
            
            
    def create_user_function(self):
        name = self.name_entry.text()
        last_name = self.last_name_entry.text()
        user_name = self.user_entry.text()
        password = self.password_entry.text()

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
            # Insertar datos en la base de datos
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (Nombre, Apellido, User, hashed_password, salt) VALUES (?, ?, ?, ?, ?)",
                           (name, last_name, user_name, hashed_password, salt))
            conn.commit()
            QMessageBox.information(self, "Éxito", "Usuario creado con éxito")
            
            # Limpiar campos de entrada
            self.name_entry.clear()
            self.last_name_entry.clear()
            self.user_entry.clear()
            self.password_entry.clear()

            # Volver a cargar los usuarios en la tabla
            self.get_user_function()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al crear usuario: {e}")

        finally:
            conn.close()
            
            
    def update_user_function(self):
        user_id = self.id_entry.text()
        name = self.name_entry.text()
        last_name = self.last_name_entry.text()
        user = self.user_entry.text()
        password = self.password_entry.text()


        hashed_password, salt = hash_password(password)
        if  verificar_len_password(password) and \
            verificar_space_password(password) and \
            verificar_capital_password(password) and \
            verificar_digit_password(password) and \
            verificar_exist_password_regist(user, password, name, last_name) and \
            verificar_illegal_character_password(password):
            pass
        else:
            QMessageBox.information(self, "Información", "Contraseña no válida. Acceso denegado.")
            return
        
        conn = establecer_conexion()
        try:
            # Actualiza el usuario en la base de datos
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET Nombre=?, Apellido=?, User=?, hashed_password=?, salt=? WHERE id=?",
                           (name, last_name, user, hashed_password, salt, user_id))
            conn.commit()
            QMessageBox.information(self, "Éxito", f"Usuario con ID {user_id} actualizado con éxito")
            
            # Limpiar campos de entrada
            self.id_entry.clear()
            self.name_entry.clear()
            self.last_name_entry.clear()
            self.user_entry.clear()
            self.password_entry.clear()

            # Volver a cargar los usuarios en la tabla
            self.get_user_function()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar usuario: {e}")

        finally:
            conn.close()
            
            
    def delete_user_function(self):
        user_id = self.id_entry.text()

        if not user_id:
            QMessageBox.critical(self, "Error", "Por favor, proporciona un ID de usuario.")
            return
        
        conn = establecer_conexion()
        try:
            # Verificar si el usuario con el ID dado existe
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id=?", (user_id,))
            user = cursor.fetchone()
            if not user:
                QMessageBox.information(self, "Información", f"El usuario con ID {user_id} no existe.")
                return
            
            # Elimina el usuario de la base de datos
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id=?", (user_id,))
            conn.commit()
            QMessageBox.information(self, "Éxito", f"Usuario con ID {user_id} eliminado con éxito")
            
            # Limpiar campos de entrada
            self.id_entry.clear()

            # Volver a cargar los usuarios en la tabla
            self.get_user_function()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar usuario: {e}")

        finally:
            conn.close()
            
    def update_progress_bar(self):
        conn = establecer_conexion()
        try:
            # Contar la cantidad de usuarios registrados
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(id) FROM usuarios")
            count = cursor.fetchone()[0]

            # Actualizar el valor de la barra de progreso
            self.progress_db_bar.setValue(count)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al obtener usuarios: {e}")

        finally:
            conn.close()
            
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = AdminGUI()
    mi_app.show()
    sys.exit(app.exec_())