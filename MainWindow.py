from PyQt5.QtWidgets import QMainWindow
from kazoo.client import KazooClient
import ui.ui_MainWindow as ui_MainWindow


class MainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.zk = KazooClient(hosts='127.0.0.1:2181')
        self.start.clicked.connect(self.startClicked)
        self.stop.clicked.connect(self.stopClicked)

    def startClicked(self):
        self.zk.start()

    def stopClicked(self):
        self.zk.stop()
