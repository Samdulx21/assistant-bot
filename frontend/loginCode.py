import sys
import re
import mysql.connector
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot
from Interfaces.Login import Ui_Form
from dashboard import dashboard

class Login(QDialog):
    def __init__(self):
        super().__init__()

        # Configura la interfaz de usuario
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Conectar la señal clicked del botón a la función correspondiente
        self.ui.pushButton.clicked.connect(self.on_login_clicked)

    def validate_email(self, email):
        # Expresión regular para validar el correo electrónico
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None    

    @pyqtSlot()
    def on_login_clicked(self):
        # Obtener los datos del Correo y Contraseña
        email = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

         # Validar el correo electrónico
        if not self.validate_email(email):
            self.ui.label_4.setText("Correo electrónico inválido.")
            return
        
        # Verificar las credenciales en la base de datos MySQL
        if not self.check_credentials(email, password):
            QMessageBox.warning(self, "Error", "Usuario no registrado.")
            return

        # Si el correo es válido, limpiar el mensaje de error
        self.ui.label_4.clear()
        # Si el correo es válido, abrir la segunda ventana (dashboard)
        self.dashboard_window = dashboard()  # Mantener referencia a la ventana del dashboard
        self.dashboard_window.show()
        self.hide()  # Ocultar la ventana de inicio de sesión

        # Imprimir los valores en la consola
        print("Correo:", email)
        print("Contraseña:", password)
        
    def check_credentials(self, email, password):
        # Conexión a la base de datos MySQL
        try:
            mybd = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="medical_center"
        )
            cursor = mybd.cursor()

            # Consulta para verificar las credenciales
            cursor.execute("""
                    SELECT u.id, u.name, u.last_name, r.description as role, u.email, u.personal_id as cc
                    FROM 
                        users u
                    JOIN
                        role_users ru ON u.id = ru.user_id
                    JOIN
                        roles r ON ru.role_id = r.id
                    WHERE 
                        u.email = %s AND u.user_password = %s""", (email, password))
          
            user = cursor.fetchall()
            payload = []
            content = {}
            for item in user:
                content = {
                    "id": item[0],
                    "name": item[1],
                    "last_name": item[2],
                    "role": item[3],
                    "email": item[4],
                    "cc": item[5],
                }
                payload.append(content)
                content = {}

            print(payload)

            mybd.close()

            return user is not None
        except mysql.connector.Error as err:
            print("Error de MySQL:", err)
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Login()
    ventana.show()
    sys.exit(app.exec_())
