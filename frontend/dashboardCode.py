import sys
import requests
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtCore import pyqtSlot
from Interfaces.Dashboard import Ui_Form

class dashboard(QDialog):
    def __init__(self, name_label_text):
        super().__init__()

        # Configura la interfaz de usuario
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Configura el texto del label con el nombre y apellido recibidos
        self.ui.label_3.setText(name_label_text)

        # Obtener el QLabel existente por su ID
        self.label_response = self.findChild(QLabel, "label_4")

         # Establecer el texto del QLabel como vacío por defecto
        self.label_response.setText("")


        # Obtener el QLineEdit existente por su ID
        self.line_edit = self.findChild(QLineEdit, "lineEdit")
        self.line_edit.returnPressed.connect(self.send_message) 

    def send_message(self):
        # Obtener el mensaje del LineEdit
        message = self.line_edit.text()

        # Enviar el mensaje a la ruta /jarvi
        url = "http://localhost:8000/jarvi"  # Reemplaza esto con la URL correcta de tu servidor
        data = {"message": message}
        response = requests.post(url, json=data)

        # Capturar y mostrar la respuesta por consola
        if response.status_code == 200:
            response_data = response.json()
            print("Respuesta del servidor:", response_data)

            # Mostrar la respuesta en el QLabel
            if "response" in response_data:
                response_text = response_data["response"]
                self.label_response.setText(response_text)
            elif "question" in response_data:
                question_text = response_data["question"]
                self.label_response.setText(question_text)

            # Limpiar el contenido del LineEdit
            self.line_edit.clear()
        else:
            print("Error al comunicarse con el servidor:", response.status_code)      


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = dashboard()
    ventana.show()
    sys.exit(app.exec_())

