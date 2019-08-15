import os

from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QPlainTextEdit, QInputDialog
from kazoo.client import KazooClient
from kazoo.client import KazooState

import ui.ui_MainWindow as ui_MainWindow


class MainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.zk = None
        self.treeWidget.itemClicked.connect(self.itemClicked)
        self.treeWidget.itemDoubleClicked.connect(self.itemOpen)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.actionConnect.triggered.connect(self.zkConnect)
        self.actionDisconnect.triggered.connect(self.zkDisconnect)
        self.actionACLVersion.triggered.connect(self.aclVersion)
        self.actionCreated.triggered.connect(self.created)
        self.actionChildrenCount.triggered.connect(self.childrenCount)
        self.actionDataLength.triggered.connect(self.dataLength)
        self.actionLastModified.triggered.connect(self.lastModified)
        self.actionLastModifiedTransactionId.triggered.connect(self.lastModifiedTransactionId)
        self.actionOwnerSessionId.triggered.connect(self.ownerSessionId)
        self.actionVersion.triggered.connect(self.version)
        self.actionCreationTransactionId.triggered.connect(self.creationTransactionId)
        self.actionChangeServerAddress.triggered.connect(self.changeServerAddress)
        self.treeWidget.setColumnCount(1)

        self.actionConnect.setEnabled(False)
        if os.path.exists("hosts.txt"):
            with open("hosts.txt", "r") as f:
                self.actionConnect.setEnabled(f.readline() != "")
    def getCurrentStat(self):
        _, stat = self.zk.get(self.treeWidget.currentItem().text(1))
        return stat

    def aclVersion(self):
        self.log.setPlainText(self.log.toPlainText() + "ACL version: %s\n" % self.getCurrentStat().acl_version)

    def created(self):
        self.log.setPlainText(self.log.toPlainText() + "Created: %s\n" % self.getCurrentStat().created)

    def childrenCount(self):
        self.log.setPlainText(self.log.toPlainText() + "Children count: %s\n" % self.getCurrentStat().children_count)

    def dataLength(self):
        self.log.setPlainText(self.log.toPlainText() + "Data length: %s\n" % self.getCurrentStat().data_length)

    def lastModified(self):
        self.log.setPlainText(self.log.toPlainText() + "Last modified: %s\n" % self.getCurrentStat().last_modified)

    def lastModifiedTransactionId(self):
        self.log.setPlainText(self.log.toPlainText() + "Last modified transactionId: %s\n" % self.getCurrentStat().last_modified_transaction_id)

    def ownerSessionId(self):
        self.log.setPlainText(self.log.toPlainText() + "Owner sessionId: %s\n" % self.getCurrentStat().owner_session_id)

    def version(self):
        self.log.setPlainText(self.log.toPlainText() + "Version: %s\n" % self.getCurrentStat().version)

    def creationTransactionId(self):
        self.log.setPlainText(self.log.toPlainText() + "Creation transactionId: %s\n" % self.getCurrentStat().creation_transaction_id)

    def changeServerAddress(self):
        text, ok = QInputDialog.getText(self, "Change server address", "Type your address and port")
        if ok:
            with open("hosts.txt", "w") as f:
                f.write(text)
            self.actionConnect.setEnabled(text != "")

    def zkDisconnect(self):
        self.tabWidget.clear()
        self.treeWidget.clear()
        self.zk.stop()
        self.zk.close()
        self.actionDisconnect.setEnabled(False)
        self.menuFileInfo.setEnabled(False)
        self.actionConnect.setEnabled(True)
        self.actionChangeServerAddress.setEnabled(True)

    def zkConnect(self):
        with open("hosts.txt", "r") as f:
            hosts = "".join(f.readlines())
            self.zk = KazooClient(hosts=hosts)
        self.zk.add_listener(self.my_listener)
        self.zk.start()
        self.init()
        self.menuFileInfo.setEnabled(True)
        self.actionDisconnect.setEnabled(True)
        self.actionConnect.setEnabled(False)
        self.actionChangeServerAddress.setEnabled(False)

    def init(self):
        for child in self.zk.get_children("/"):
            self.treeWidget.addTopLevelItem(QTreeWidgetItem([child, "/" + child]))

    def my_listener(self, state):
        if state == KazooState.LOST:
            # Register somewhere that the session was lost
            self.log.setPlainText(self.log.toPlainText() + "state is LOST!\n")
        elif state == KazooState.SUSPENDED:
            # Handle being disconnected from Zookeeper
            self.log.setPlainText(self.log.toPlainText() + "state is SUSPENDED!\n")
        else:
            # Handle being connected/reconnected to Zookeeper
            self.log.setPlainText(self.log.toPlainText() + "state is CONNECTED!\n")

    def printAllChildren(self, curPath, children, layer):
        spaces = "  " * layer
        for child in children:
            newPath = curPath + "/" + child
            data, stat = self.zk.get(newPath)
            self.log.setPlainText(self.log.toPlainText() + "%s: %s\n" % (spaces + child, data))
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
            self.log.setPlainText(self.log.toPlainText() + "Really?.. How?.. Why?..\n")

    def itemClicked(self, item, column):
        item.takeChildren()
        if self.zk.exists(item.text(1)):
            for child in self.zk.get_children(item.text(1)):
                item.addChild(QTreeWidgetItem([child, item.text(1) + "/" + child]))
