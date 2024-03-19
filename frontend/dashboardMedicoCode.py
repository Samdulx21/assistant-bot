import sys
import requests
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtCore import pyqtSlot
from Interfaces.DashboardMedico import Ui_Form

class dashboardMedico(QDialog):
    def __init__(self, name_label_text):
        super().__init__()

        # Configura la interfaz de usuario
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Configura el texto del label con el nombre y apellido recibidos
        self.ui.label_3.setText(name_label_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = dashboardMedico()
    ventana.show()
    sys.exit(app.exec_())

