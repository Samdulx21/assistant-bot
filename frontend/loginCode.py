import sys
import re
import requests
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from Interfaces.Login import Ui_Form
from dashboardCode import dashboard
from dashboardMedicoCode import dashboardMedico

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
        response = self.check_credentials(email, password)
        if "error" in response:
            QMessageBox.warning(self, "Error", "Error al verificar las credenciales.")
            return
        elif not response.get("result"):
            QMessageBox.warning(self, "Error", "Usuario no registrado.")
            return
        elif "result" in response:
            user_data = response["result"]
            print("Respuesta del servidor:", user_data)  # Imprimir la respuesta del servidor por consola

        # Si hay datos de usuario en la respuesta, mostrarlos en el label
        if user_data:
            user_info = user_data[0]  # Tomar el primer usuario de la lista si hay varios
            name = user_info.get("name", "")
            last_name = user_info.get("last_name", "")
            name_label_text = f"{name} {last_name}"
           # self.ui.label_3.setText("samuel dulce")  # Configurar el texto del label
            print("Texto del label_3:", name_label_text)  # Imprimir el texto del label por consola

            role = user_info.get("role", "")
            print("Role del usuario:", role)  # Imprimir el valor de role por consola

            if role == "Role Medico":
                # Mostrar la ventana del dashboard del médico
                self.dashboard_medico_window = dashboardMedico(name_label_text)
                self.dashboard_medico_window.show()
            else:
                # Mostrar la ventana del dashboard del paciente
                self.dashboard_window = dashboard(name_label_text)
                self.dashboard_window.show()
                
            self.hide()    


        # Si el correo es válido, limpiar el mensaje de error
        self.ui.label_4.clear()
        # Si el correo es válido, abrir la segunda ventana (dashboard)
       # self.dashboard_window = dashboard(name_label_text)  # Mantener referencia a la ventana del dashboard
       # self.dashboard_window.show()
       # self.hide()  # Ocultar la ventana de inicio de sesión

        # Imprimir los valores en la consola
        print("Correo:", email)
        print("Contraseña:", password)
        
    def check_credentials(self, email, password):
        # Envio de datos a la ruta login
        try:
            url = "http://localhost:8000/login"  # URL de la ruta de login en tu backend
            data = {"email": email, "user_password": password}
            response = requests.post(url, json=data)
            print(response)
            return response.json()
        except Exception as e:
            print("Error al hacer la solicitud al backend:", e)
            return {"error": "Error al hacer la solicitud al backend"}
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Login()
    ventana.show()
    sys.exit(app.exec_())
