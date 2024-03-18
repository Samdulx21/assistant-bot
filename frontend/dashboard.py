import sys
import re
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot
from Interfaces.Dashboard import Ui_FormDashboard

class dashboard(QDialog):
    def __init__(self):
        super().__init__()

        # Configura la interfaz de usuario
        self.ui = Ui_FormDashboard()
        self.ui.setupUi(self)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = dashboard()
    ventana.show()
    sys.exit(app.exec_())
