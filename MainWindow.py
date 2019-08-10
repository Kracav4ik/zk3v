from PyQt5.QtWidgets import QMainWindow
import ui.ui_MainWindow as ui_MainWindow


class MainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
