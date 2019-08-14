from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QPlainTextEdit, QWidget
from kazoo.client import KazooClient
from kazoo.client import KazooState

import ui.ui_MainWindow as ui_MainWindow


class MainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.zk = KazooClient(hosts='127.0.0.1:2181')
        self.zk.start()
        self.treeWidget.itemClicked.connect(self.itemClicked)
        self.treeWidget.itemDoubleClicked.connect(self.itemOpen)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.zk.add_listener(self.my_listener)
        self.treeWidget.setColumnCount(1)
        for child in self.zk.get_children("/"):
            self.treeWidget.addTopLevelItem(QTreeWidgetItem([child, "/" + child]))

    def my_listener(self, state):
        if state == KazooState.LOST:
            self.log.appendPlainText("state is LOST!\n")
        # Register somewhere that the session was lost
        elif state == KazooState.SUSPENDED:
            self.log.appendPlainText("state is SUSPENDED!\n")
        # Handle being disconnected from Zookeeper
        else:
            self.log.appendPlainText("state is CONNECTED!\n")

        # Handle being connected/reconnected to Zookeeper

    def printAllChildren(self, curPath, children, layer):
        spaces = "  " * layer
        for child in children:
            newPath = curPath + "/" + child
            data, stat = self.zk.get(newPath)
            self.log.appendPlainText("%s: %s\n" % (spaces + child, data))
            self.printAllChildren(newPath, self.zk.get_children(newPath), layer + 1)

    def closeTab(self, idx):
        self.tabWidget.removeTab(idx)

    def itemOpen(self, item, column):
        tabName = item.text(0)
        for i in range(self.tabWidget.count()):
            if tabName == self.tabWidget.tabText(i):
                self.tabWidget.setCurrentIndex(i)
                return
        innerText = QPlainTextEdit()
        innerText.setReadOnly(True)
        data, stat = self.zk.get(item.text(1))
        innerText.setPlainText(data.decode("utf8"))
        pos = self.tabWidget.addTab(innerText, tabName)
        self.tabWidget.setCurrentIndex(pos)


    def drawAllTree(self):
        if self.zk.exists("/"):
            root = self.zk.get_children("/")
            self.printAllChildren("/", root, 0)
        else:
            self.log.appendPlainText("Really?.. How?.. Why?..\n")

    def itemClicked(self, item, column):
        item.takeChildren()
        if self.zk.exists(item.text(1)):
            for child in self.zk.get_children(item.text(1)):
                item.addChild(QTreeWidgetItem([child, item.text(1) + "/" + child]))
