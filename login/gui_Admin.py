from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox


from chat import speaks
import datetime
from conection.conexion import establecer_conexion, establecer_conexion_log
from voices.voices import talk
from security.protect import (hash_password, 
                              verificar_len_password, 
                              verificar_capital_password, 
                              verificar_digit_password, 
                              verificar_illegal_character_password, 
                              verificar_space_password, 
                              verificar_exist_password_regist,
                              validar_correo_electronico,
                              validar_telefono_movil, 
                              generate_unique_token
                              )

class Ui_AdminPanel_4(object):
    def setupUi(self, AdminPanel_4):
        AdminPanel_4.setObjectName("AdminPanel_4")
        AdminPanel_4.resize(996, 615)
        AdminPanel_4.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.centralwidget = QtWidgets.QWidget(AdminPanel_4)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1001, 621))
        AdminPanel_4.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.tabWidget.setStyleSheet("\n"
"")
        self.tabWidget.setObjectName("tabWidget")
        self.AdminPanel = QtWidgets.QWidget()
        self.AdminPanel.setObjectName("AdminPanel")
        self.btn_create = QtWidgets.QPushButton(self.AdminPanel)
        self.btn_create.setGeometry(QtCore.QRect(880, 20, 101, 31))
        self.btn_create.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_create.setStyleSheet("QPushButton {\n"
"    background-color: rgb(23, 231, 183);\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(23, 231, 183, 150);\n"
"}")
        self.btn_create.setObjectName("btn_create")
        self.btn_update = QtWidgets.QPushButton(self.AdminPanel)
        self.btn_update.setGeometry(QtCore.QRect(880, 70, 101, 31))
        self.btn_update.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_update.setStyleSheet("QPushButton {\n"
"    background-color: rgb(137, 206, 206);\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(137, 206, 206, 150);\n"
"}\n"
"")
        self.btn_update.setObjectName("btn_update")
        self.progress_db_bar = QtWidgets.QProgressBar(self.AdminPanel)
        self.progress_db_bar.setGeometry(QtCore.QRect(650, 550, 331, 23))
        self.progress_db_bar.setStyleSheet("color: rgb(255, 255, 255);")
        self.progress_db_bar.setProperty("value", 0)
        self.progress_db_bar.setObjectName("progress_db_bar")
        self.radio_button_voice = QtWidgets.QRadioButton(self.AdminPanel)
        self.radio_button_voice.setGeometry(QtCore.QRect(920, 320, 61, 17))
        self.radio_button_voice.setFocusPolicy(QtCore.Qt.NoFocus)
        self.radio_button_voice.setStyleSheet("color: rgb(255, 255, 255);")
        self.radio_button_voice.setObjectName("radio_button_voice")
        self.password_entry = QtWidgets.QLineEdit(self.AdminPanel)
        self.password_entry.setGeometry(QtCore.QRect(750, 260, 113, 20))
        self.password_entry.setObjectName("password_entry")
        self.radio_button_manul = QtWidgets.QRadioButton(self.AdminPanel)
        self.radio_button_manul.setGeometry(QtCore.QRect(840, 320, 71, 17))
        self.radio_button_manul.setFocusPolicy(QtCore.Qt.NoFocus)
        self.radio_button_manul.setStyleSheet("color: rgb(255, 255, 255);")
        self.radio_button_manul.setObjectName("radio_button_manul")
        self.btn_run = QtWidgets.QPushButton(self.AdminPanel)
        self.btn_run.setGeometry(QtCore.QRect(880, 240, 101, 31))
        self.btn_run.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_run.setStyleSheet("QPushButton {\n"
"    background-color: rgb(181, 181, 181);\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(181, 181, 181, 150);\n"
"}\n"
"")
        self.btn_run.setObjectName("btn_run")
        self.name_label = QtWidgets.QLabel(self.AdminPanel)
        self.name_label.setGeometry(QtCore.QRect(660, 60, 61, 21))
        self.name_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.name_label.setObjectName("name_label")
        self.name_entry = QtWidgets.QLineEdit(self.AdminPanel)
        self.name_entry.setGeometry(QtCore.QRect(750, 60, 113, 20))
        self.name_entry.setObjectName("name_entry")
        self.email_label = QtWidgets.QLabel(self.AdminPanel)
        self.email_label.setGeometry(QtCore.QRect(660, 140, 51, 21))
        self.email_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.email_label.setObjectName("email_label")
        self.last_name_entry = QtWidgets.QLineEdit(self.AdminPanel)
        self.last_name_entry.setGeometry(QtCore.QRect(750, 100, 113, 20))
        self.last_name_entry.setObjectName("last_name_entry")
        self.id_label = QtWidgets.QLabel(self.AdminPanel)
        self.id_label.setGeometry(QtCore.QRect(660, 20, 31, 21))
        self.id_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.id_label.setObjectName("id_label")
        self.user_label = QtWidgets.QLabel(self.AdminPanel)
        self.user_label.setGeometry(QtCore.QRect(660, 220, 51, 21))
        self.user_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.user_label.setObjectName("user_label")
        self.phone_entry = QtWidgets.QLineEdit(self.AdminPanel)
        self.phone_entry.setGeometry(QtCore.QRect(750, 180, 111, 20))
        self.phone_entry.setObjectName("phone_entry")
        # self.phone_entry.setPlaceholderText("Ejm: +34763532456")
        self.storage_db_label = QtWidgets.QLabel(self.AdminPanel)
        self.storage_db_label.setGeometry(QtCore.QRect(650, 520, 81, 21))
        self.storage_db_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.storage_db_label.setObjectName("storage_db_label")
        self.btn_get = QtWidgets.QPushButton(self.AdminPanel)
        self.btn_get.setGeometry(QtCore.QRect(880, 170, 101, 31))
        self.btn_get.setMouseTracking(False)
        self.btn_get.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_get.setStyleSheet("QPushButton {\n"
"    background-color: rgb(226, 226, 112);\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(226, 226, 112, 150);\n"
"}\n"
"")
        self.btn_get.setObjectName("btn_get")
        self.last_name_label = QtWidgets.QLabel(self.AdminPanel)
        self.last_name_label.setGeometry(QtCore.QRect(660, 100, 71, 21))
        self.last_name_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.last_name_label.setObjectName("last_name_label")
        self.list_widget_terminal = QtWidgets.QListWidget(self.AdminPanel)
        self.list_widget_terminal.setGeometry(QtCore.QRect(650, 350, 331, 161))
        self.list_widget_terminal.setObjectName("list_widget_terminal")
        self.email_entry = QtWidgets.QLineEdit(self.AdminPanel)
        self.email_entry.setGeometry(QtCore.QRect(750, 140, 113, 20))
        self.email_entry.setObjectName("email_entry")
        self.table_widget_principal = QtWidgets.QTableWidget(self.AdminPanel)
        self.table_widget_principal.setGeometry(QtCore.QRect(10, 10, 631, 571))
        self.table_widget_principal.setObjectName("table_widget_principal")
        self.table_widget_principal.setColumnCount(0)
        self.table_widget_principal.setRowCount(0)
        self.btn_delete = QtWidgets.QPushButton(self.AdminPanel)
        self.btn_delete.setGeometry(QtCore.QRect(880, 120, 101, 31))
        self.btn_delete.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_delete.setStyleSheet("QPushButton {\n"
"    background-color: rgb(193, 0, 0);\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(193, 0, 0, 150);\n"
"}\n"
"")
        self.btn_delete.setObjectName("btn_delete")
        self.user_entry = QtWidgets.QLineEdit(self.AdminPanel)
        self.user_entry.setGeometry(QtCore.QRect(750, 220, 113, 20))
        self.user_entry.setObjectName("user_entry")
        self.mode_label = QtWidgets.QLabel(self.AdminPanel)
        self.mode_label.setGeometry(QtCore.QRect(880, 290, 101, 21))
        self.mode_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.mode_label.setObjectName("mode_label")
        self.password_label = QtWidgets.QLabel(self.AdminPanel)
        self.password_label.setGeometry(QtCore.QRect(660, 260, 81, 21))
        self.password_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.password_label.setObjectName("password_label")
        self.id_entry = QtWidgets.QLineEdit(self.AdminPanel)
        self.id_entry.setGeometry(QtCore.QRect(750, 20, 113, 20))
        self.id_entry.setObjectName("id_entry")
        self.phone_label = QtWidgets.QLabel(self.AdminPanel)
        self.phone_label.setGeometry(QtCore.QRect(660, 180, 61, 21))
        self.phone_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.phone_label.setObjectName("phone_label")
        self.frame = QtWidgets.QFrame(self.AdminPanel)
        self.frame.setGeometry(QtCore.QRect(-1, -21, 1001, 611))
        self.frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x3:1, y2:2, stop:0 rgba(10, 38, 31, 255), stop:1 rgba(1, 229, 161, 255));")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.raise_()
        self.btn_create.raise_()
        self.btn_update.raise_()
        self.progress_db_bar.raise_()
        self.radio_button_voice.raise_()
        self.password_entry.raise_()
        self.radio_button_manul.raise_()
        self.btn_run.raise_()
        self.name_label.raise_()
        self.name_entry.raise_()
        self.email_label.raise_()
        self.last_name_entry.raise_()
        self.id_label.raise_()
        self.user_label.raise_()
        self.phone_entry.raise_()
        self.storage_db_label.raise_()
        self.btn_get.raise_()
        self.last_name_label.raise_()
        self.list_widget_terminal.raise_()
        self.email_entry.raise_()
        self.table_widget_principal.raise_()
        self.btn_delete.raise_()
        self.user_entry.raise_()
        self.mode_label.raise_()
        self.password_label.raise_()
        self.id_entry.raise_()
        self.phone_label.raise_()
        self.tabWidget.addTab(self.AdminPanel, "")
        self.AdminLogs = QtWidgets.QWidget()
        self.AdminLogs.setObjectName("AdminLogs")
        self.listView_logs = QtWidgets.QListWidget(self.AdminLogs)
        self.listView_logs.setGeometry(QtCore.QRect(10, 10, 971, 192))
        self.listView_logs.setObjectName("listView_logs")
        self.pushButton_logs = QtWidgets.QPushButton(self.AdminLogs)
        self.pushButton_logs.setGeometry(QtCore.QRect(850, 220, 130, 31))
        self.pushButton_logs.setStyleSheet("QPushButton {\n"
"    background-color: rgb(181, 181, 181);\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(181, 181, 181, 150);\n"
"}\n"
"")
        self.pushButton_logs.setObjectName("pushButton_logs")
        self.frame_2 = QtWidgets.QFrame(self.AdminLogs)
        self.frame_2.setGeometry(QtCore.QRect(-1, -31, 1001, 621))
        self.frame_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x3:1, y2:2, stop:0 rgba(10, 38, 31, 255), stop:1 rgba(1, 229, 161, 255));")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.raise_()
        self.listView_logs.raise_()
        self.pushButton_logs.raise_()
        self.tabWidget.addTab(self.AdminLogs, "")
        AdminPanel_4.setCentralWidget(self.centralwidget)
        self.actionAdmin_Panel = QtWidgets.QAction(AdminPanel_4)
        self.actionAdmin_Panel.setObjectName("actionAdmin_Panel")

        self.retranslateUi(AdminPanel_4)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AdminPanel_4)

    def retranslateUi(self, AdminPanel_4):
        _translate = QtCore.QCoreApplication.translate
        AdminPanel_4.setWindowTitle(_translate("AdminPanel_4", "MainWindow"))
        self.btn_create.setText(_translate("AdminPanel_4", "Create"))
        self.btn_update.setText(_translate("AdminPanel_4", "Update"))
        self.radio_button_voice.setText(_translate("AdminPanel_4", "Voice"))
        self.radio_button_manul.setText(_translate("AdminPanel_4", "Manual"))
        self.btn_run.setText(_translate("AdminPanel_4", "Run"))
        self.name_label.setText(_translate("AdminPanel_4", "Name :"))
        self.email_label.setText(_translate("AdminPanel_4", "Email :"))
        self.id_label.setText(_translate("AdminPanel_4", "ID :"))
        self.user_label.setText(_translate("AdminPanel_4", "User :"))
        self.storage_db_label.setText(_translate("AdminPanel_4", "Storage DB"))
        self.btn_get.setText(_translate("AdminPanel_4", "Get"))
        self.last_name_label.setText(_translate("AdminPanel_4", "Last Name :"))
        self.btn_delete.setText(_translate("AdminPanel_4", "Delete"))
        self.mode_label.setText(_translate("AdminPanel_4", "Startup Mode"))
        self.password_label.setText(_translate("AdminPanel_4", "Password :"))
        self.phone_label.setText(_translate("AdminPanel_4", "Phone :"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AdminPanel), _translate("AdminPanel_4", "Tab 1"))
        self.pushButton_logs.setText(_translate("AdminPanel_4", "Dell Logs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AdminLogs), _translate("AdminPanel_4", "Tab 2"))
        self.actionAdmin_Panel.setText(_translate("AdminPanel_4", "Admin-Panel"))
        
        self.conn = establecer_conexion_log()
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, timestamp TEXT, action TEXT)''')
        self.conn.commit()

        self.u = QtWidgets.QMainWindow()
        self.btn_get.clicked.connect(self.get_user_function)
        self.btn_create.clicked.connect(self.create_user_function)
        self.btn_update.clicked.connect(self.update_user_function)
        self.btn_delete.clicked.connect(self.delete_user_function)
        # self.btn_run.clicked.connect(speaks.run(False))
        
        # self.radio_button_manul.clicked.connect(lambda: speaks.run(False))
        # self.radio_button_voice.clicked.connect(lambda: speaks.run(True))
        
        # self.setWindowTitle("Admin-Panel")
        # self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        
    def get_user_function(self):
            
        conn = establecer_conexion()
        try:
            # Obtener datos de la base de datos
            cursor = conn.cursor()
            cursor.execute("SELECT id, Nombre, Apellido, Email, Telefono, User FROM usuarios")
            users = cursor.fetchall()

            if not users:
                QMessageBox.information(self.u, "Información", "No hay información de usuarios disponible.")
            else:
                # Limpiar la tabla antes de agregar elementos nuevos
                self.table_widget_principal.clearContents()
                self.table_widget_principal.setRowCount(0)
                
                # Agregar cabeceras
                headers = ["ID", "Nombre", "Apellido", "Email", "Telefono", "Usuario"]
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
            QMessageBox.critical(self.u, "Error", f"Error al obtener usuarios: {e}")

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
            QMessageBox.critical(self.u, "Error", f"Error al obtener usuarios: {e}")

        finally:
            conn.close()

    def create_user_function(self):
        name = self.name_entry.text()
        last_name = self.last_name_entry.text()
        email = self.email_entry.text()
        telf = self.phone_entry.text()
        user_name = self.user_entry.text()
        password = self.password_entry.text()
        

        hashed_password, salt = hash_password(password)
        if verificar_len_password(password) and \
           verificar_space_password(password) and \
           verificar_capital_password(password) and \
           verificar_digit_password(password) and \
           verificar_exist_password_regist(user_name, password, name, last_name) and \
           validar_telefono_movil(telf) and \
           validar_correo_electronico(email) and \
           verificar_illegal_character_password(password):
            pass
        else:
            talk("Contraseña no válida. Acceso denegado.")
            return
        conn = establecer_conexion()
        try:
            unique_token = generate_unique_token()
            
            # Insertar datos en la base de datos
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (Nombre, Apellido, Email, Telefono, User, hashed_password, salt, Token) VALUES (?, ?, ?, ?, ?, ?, ?)', (name, last_name, email, telf, user_name, hashed_password, salt, unique_token))
            conn.commit()
            QMessageBox.information(self.u, "Éxito", "Usuario creado con éxito")
            action = 'Create_User'
            self.log("Admin", action)
            self.show_logs()
            
            # Limpiar campos de entrada
            self.name_entry.clear()
            self.last_name_entry.clear()
            self.email_entry.clear()
            self.phone_entry.clear()
            self.user_entry.clear()
            self.password_entry.clear()

            # Volver a cargar los usuarios en la tabla
            self.get_user_function()

        except Exception as e:
            QMessageBox.critical(self.u, "Error", f"Error al crear usuario: {e}")

        finally:
            conn.close()
            
            
    def update_user_function(self):
        user_id = self.id_entry.text()
        name = self.name_entry.text()
        last_name = self.last_name_entry.text()
        email = self.email_entry.text()
        telf = self.phone_entry.text()
        user_name = self.user_entry.text()
        password = self.password_entry.text()


        hashed_password, salt = hash_password(password)
        if verificar_len_password(password) and \
           verificar_space_password(password) and \
           verificar_capital_password(password) and \
           verificar_digit_password(password) and \
           verificar_exist_password_regist(user_name, password, name, last_name) and \
           validar_telefono_movil(telf) and \
           validar_correo_electronico(email) and \
           verificar_illegal_character_password(password):
            pass
        else:
            QMessageBox.information(self.u, "Información", "Contraseña no válida. Acceso denegado.")
            return
        
        conn = establecer_conexion()
        try:
            # Actualiza el usuario en la base de datos
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET Nombre=?, Apellido=?, Email=?, Telefono=?, User=?, hashed_password=?, salt=? WHERE id=?",
                           (name, last_name, email, telf, user_name, hashed_password, salt, user_id))
            conn.commit()
            QMessageBox.information(self.u, "Éxito", f"Usuario con ID {user_id} actualizado con éxito")
            action = 'Update_User'
            self.log("Admin", action)
            self.show_logs()
            
            # Limpiar campos de entrada
            self.id_entry.clear()
            self.name_entry.clear()
            self.last_name_entry.clear()
            self.email_entry.clear()
            self.phone_entry.clear()
            self.user_entry.clear()
            self.password_entry.clear()

            # Volver a cargar los usuarios en la tabla
            self.get_user_function()

        except Exception as e:
            QMessageBox.critical(self.u, "Error", f"Error al actualizar usuario: {e}")

        finally:
            conn.close()
            
            
    def delete_user_function(self):
        user_id = self.id_entry.text()

        if not user_id:
            QMessageBox.critical(self.u, "Error", "Por favor, proporciona un ID de usuario.")
            return
        
        conn = establecer_conexion()
        try:
            # Verificar si el usuario con el ID dado existe
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id=?", (user_id,))
            user = cursor.fetchone()
            if not user:
                QMessageBox.information(self.u, "Información", f"El usuario con ID {user_id} no existe.")
                return
            
            # Elimina el usuario de la base de datos
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id=?", (user_id,))
            conn.commit()
            QMessageBox.information(self.u, "Éxito", f"Usuario con ID {user_id} eliminado con éxito")
            action = 'Delete_User'
            self.log("Admin", action)
            self.show_logs()
            
            # Limpiar campos de entrada
            self.id_entry.clear()

            # Volver a cargar los usuarios en la tabla
            self.get_user_function()

        except Exception as e:
            QMessageBox.critical(self.u, "Error", f"Error al eliminar usuario: {e}")

        finally:
            conn.close()
            
    def log(self, user, action):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = (user , timestamp, action)
        self.cursor.execute('INSERT INTO logs (user, timestamp, action) VALUES (?, ?, ?)', data)
        self.conn.commit()
        
    def get_log(self):
        self.cursor.execute('SELECT * FROM logs')
        return self.cursor.fetchall()
    
    def show_logs(self):
        self.listView_logs.clear()
        self.cursor.execute('SELECT * FROM logs')
        for row in self.cursor.fetchall():
            item = f'User: {row[1]} | Timestamp: {row[2]} | Action: {row[3]}'
            self.listView_logs.addItem(item)