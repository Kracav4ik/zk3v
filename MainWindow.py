import functools
import traceback
import logging
import os
import sys

from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QPlainTextEdit, QInputDialog, QMessageBox, QProgressBar
from kazoo.client import KazooClient
from kazoo.client import KazooState

import ui.ui_MainWindow as ui_MainWindow


def catchExept(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logging.exception("error: {0}".format(e))
    return wrap


class MainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    @catchExept
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.zk = KazooClient()
        self.msgBox = QMessageBox(QMessageBox.NoIcon, "Connection", "Connecting...", QMessageBox.Cancel, self)
        self.treeWidget.itemClicked.connect(self.itemClicked)
        self.treeWidget.itemDoubleClicked.connect(self.itemOpen)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.actionConnect.triggered.connect(self.msgBox.show)
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
        self.msgBox.buttonClicked.connect(self.msgBox.hide)
        self.msgBox.buttonClicked.connect(self.zkDisconnect)

        class PlainTextWidgetHandler:
            def __init__(self, plainTextWidget):
                self.plainTextWidget = plainTextWidget
                self.plainTextWidget.setCenterOnScroll(True)

            def write(self, text):
                self.plainTextWidget.ensureCursorVisible()
                self.plainTextWidget.textCursor().insertText(text)

            def flush(self):
                pass

        logging.basicConfig(format='%(asctime)s.%(msecs)d: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG,
                            handlers=[logging.StreamHandler(PlainTextWidgetHandler(self.log)),
                                      logging.StreamHandler(sys.stderr)])

        self.treeWidget.setColumnCount(1)
        self.currentHost = ""

        l = self.msgBox.layout()
        progress = QProgressBar()
        progress.setMaximum(0)
        progress.setMinimum(0)
        l.addWidget(progress, l.rowCount() - 2, 1, 1, l.columnCount())

        self.actionConnect.setEnabled(False)
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as f:
                self.currentHost = f.readline().strip()
                if self.currentHost != "":
                    self.print("Current host is: %s" % self.currentHost)
                    self.actionConnect.setEnabled(True)
    @catchExept
    def getCurrentStat(self):
        _, stat = self.zk.get(self.treeWidget.currentItem().text(1))
        return stat

    @catchExept
    @pyqtSlot()
    def aclVersion(self):
        self.print("ACL version: %s" % self.getCurrentStat().acl_version)

    @catchExept
    @pyqtSlot()
    def created(self):
        self.print("Created: %s" % self.getCurrentStat().created)

    @catchExept
    @pyqtSlot()
    def childrenCount(self):
        self.print("Children count: %s" % self.getCurrentStat().children_count)

    @catchExept
    @pyqtSlot()
    def dataLength(self):
        self.print("Data length: %s" % self.getCurrentStat().data_length)

    @catchExept
    @pyqtSlot()
    def lastModified(self):
        self.print("Last modified: %s" % self.getCurrentStat().last_modified)

    @catchExept
    @pyqtSlot()
    def lastModifiedTransactionId(self):
        self.print("Last modified transactionId: %s" % self.getCurrentStat().last_modified_transaction_id)

    @catchExept
    @pyqtSlot()
    def ownerSessionId(self):
        self.print("Owner sessionId: %s" % self.getCurrentStat().owner_session_id)

    @catchExept
    @pyqtSlot()
    def version(self):
        self.print("Version: %s" % self.getCurrentStat().version)

    @catchExept
    @pyqtSlot()
    def creationTransactionId(self):
        self.print("Creation transactionId: %s" % self.getCurrentStat().creation_transaction_id)

    @catchExept
    @pyqtSlot()
    def changeServerAddress(self):
        text, ok = QInputDialog.getText(self, "Change server address", "Type your address and port",
                                        text=self.currentHost)
        if ok:
            with open("config.txt", "w") as f:
                f.write(text)
            self.currentHost = text.strip()
            if self.currentHost != "":
                self.print("Current host changed to %s" % self.currentHost)
                self.actionConnect.setEnabled(True)

    @catchExept
    @pyqtSlot()
    def zkDisconnect(self):
        self.tabWidget.clear()
        self.treeWidget.clear()
        self.zk.stop()
        self.zk.close()
        self.actionDisconnect.setEnabled(False)
        self.menuFileInfo.setEnabled(False)
        self.actionConnect.setEnabled(True)
        self.actionChangeServerAddress.setEnabled(True)

    @catchExept
    @pyqtSlot()
    def zkConnect(self):
        self.zk.set_hosts(self.currentHost)
        self.zk.add_listener(self.my_listener)
        try:
            self.zk.start()
        except Exception as e:
            logging.exception("error: {0}".format(e))
        finally:
            self.msgBox.hide()
        self.init()
        self.menuFileInfo.setEnabled(True)
        self.actionDisconnect.setEnabled(True)
        self.actionConnect.setEnabled(False)
        self.actionChangeServerAddress.setEnabled(False)

    @catchExept
    def init(self):
        for child in self.zk.get_children("/"):
            self.treeWidget.addTopLevelItem(QTreeWidgetItem([child, "/" + child]))

    @catchExept
    def my_listener(self, state):
        if state == KazooState.LOST:
            # Register somewhere that the session was lost
            self.print("state is LOST!")
        elif state == KazooState.SUSPENDED:
            # Handle being disconnected from Zookeeper
            self.print("state is SUSPENDED!")
        else:
            # Handle being connected/reconnected to Zookeeper
            self.print("state is CONNECTED!")

    @catchExept
    def print(self, text):
        logging.debug(text)

    @catchExept
    def printAllChildren(self, curPath, children, layer):
        spaces = "  " * layer
        for child in children:
            newPath = curPath + "/" + child
            data, stat = self.zk.get(newPath)
            self.print("%s: %s" % (spaces + child, data))
            self.printAllChildren(newPath, self.zk.get_children(newPath), layer + 1)

    @catchExept
    @pyqtSlot(int)
    def closeTab(self, idx):
        self.tabWidget.removeTab(idx)

    @catchExept
    @pyqtSlot(QTreeWidgetItem, int)
    def itemOpen(self, item, column):
        if not self.zk.exists(item.text(1)):
            return
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


    @catchExept
    def drawAllTree(self):
        if self.zk.exists("/"):
            root = self.zk.get_children("/")
            self.printAllChildren("/", root, 0)
        else:
            self.print("Really?.. How?.. Why?..")

    @catchExept
    @pyqtSlot(QTreeWidgetItem, int)
    def itemClicked(self, item, column):
        item.takeChildren()
        if self.zk.exists(item.text(1)):
            for child in self.zk.get_children(item.text(1)):
                item.addChild(QTreeWidgetItem([child, item.text(1) + "/" + child]))
