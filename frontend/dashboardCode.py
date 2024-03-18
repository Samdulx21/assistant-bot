import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot
from Interfaces.Dashboard import Ui_Form
from loginCode import EndPointLogic

class dashboard(QDialog):
    def __init__(self):
        super().__init__()

        # Configura la interfaz de usuario
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        
        # Conecta la señal del endpoint al método para actualizar el label
        self.end_point_logic = EndPointLogic()
        self.end_point_logic.user_info_updated.connect(self.update_label)

    def update_label(self, name, last_name):
        name_label_text = f"{name} {last_name}"
        self.ui.label_3.setText(name_label_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = dashboard()
    ventana.show()
    sys.exit(app.exec_())
