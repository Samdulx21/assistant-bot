import sys
import requests
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QLineEdit
from PyQt5.QtCore import Qt
from Interfaces.DashboardMedico import Ui_Form

class dashboardMedico(QDialog):
    def __init__(self):
        super().__init__()

        # Configura la interfaz de usuario
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Configura la señal de presionar Enter en la caja de texto
        self.ui.lineEdit.returnPressed.connect(self.update_table)

        # Llenar la tabla con todos los usuarios al iniciar
        self.populate_table()

    def populate_table(self):
        try:
            url = "http://localhost:8000/users"  # Obtener todos los usuarios
            response = requests.get(url)
            if response.status_code == 200:
                user_data = response.json()["result"]
            else:
                print("Error al obtener los datos de usuario:", response.status_code)
                return
        except Exception as e:
            print("Error al hacer la solicitud al servidor:", e)
            return
         # Configura el texto del label con el nombre y apellido recibidos
        name_label_text = f"{user_data[0]['name']} {user_data[0]['last_name']}"
        self.ui.label_3.setText(name_label_text)

        self.display_users(user_data)

    def update_table(self):
        personal_id = self.ui.lineEdit.text()
        if not personal_id:
            self.populate_table()  # Si no se ingresa cédula, mostrar todos los usuarios
            return

        try:
            url = f"http://localhost:8000/user/role/{personal_id}"  # Obtener usuario por cédula
            response = requests.get(url)
            if response.status_code == 200:
                user_data = response.json()["result"]
                self.display_users(user_data)
            else:
                print("Error al obtener los datos de usuario:", response.status_code)
        except Exception as e:
            print("Error al hacer la solicitud al servidor:", e)

    def display_users(self, user_data):
         # Configurar el número de filas y columnas de la tabla
        self.ui.tableWidget.setRowCount(len(user_data))
        self.ui.tableWidget.setColumnCount(len(user_data[0]) - 1)  # Eliminar una columna

        # Establecer los encabezados de la tabla
        headers = [key for key in user_data[0].keys() if key != 'user_password']  # Excluir 'user_password'
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)

        self.ui.tableWidget.verticalHeader().setVisible(False)  # Ocultar los números de fila

        # Rellenar la tabla con los datos del usuario
        for i, data in enumerate(user_data):
            for j, (key, value) in enumerate(data.items()):
                if key != 'user_password':  # Excluir 'user_password'
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # Hacer las celdas no editables
                    self.ui.tableWidget.setItem(i, j, item)  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = dashboardMedico()
    ventana.show()
    sys.exit(app.exec_())
