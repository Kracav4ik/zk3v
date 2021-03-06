# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(703, 497)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName("splitter_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.header().setVisible(False)
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.log = QtWidgets.QPlainTextEdit(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log.sizePolicy().hasHeightForWidth())
        self.log.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.log.setFont(font)
        self.log.setReadOnly(True)
        self.log.setObjectName("log")
        self.verticalLayout.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 703, 21))
        self.menubar.setObjectName("menubar")
        self.menuFileInfo = QtWidgets.QMenu(self.menubar)
        self.menuFileInfo.setEnabled(False)
        self.menuFileInfo.setObjectName("menuFileInfo")
        self.menuConnect = QtWidgets.QMenu(self.menubar)
        self.menuConnect.setObjectName("menuConnect")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionCreationTransactionId = QtWidgets.QAction(MainWindow)
        self.actionCreationTransactionId.setObjectName("actionCreationTransactionId")
        self.actionLastModifiedTransactionId = QtWidgets.QAction(MainWindow)
        self.actionLastModifiedTransactionId.setObjectName("actionLastModifiedTransactionId")
        self.actionCreated = QtWidgets.QAction(MainWindow)
        self.actionCreated.setObjectName("actionCreated")
        self.actionLastModified = QtWidgets.QAction(MainWindow)
        self.actionLastModified.setObjectName("actionLastModified")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actionACLVersion = QtWidgets.QAction(MainWindow)
        self.actionACLVersion.setObjectName("actionACLVersion")
        self.actionOwnerSessionId = QtWidgets.QAction(MainWindow)
        self.actionOwnerSessionId.setObjectName("actionOwnerSessionId")
        self.actionDataLength = QtWidgets.QAction(MainWindow)
        self.actionDataLength.setObjectName("actionDataLength")
        self.actionChildrenCount = QtWidgets.QAction(MainWindow)
        self.actionChildrenCount.setObjectName("actionChildrenCount")
        self.actionConnect = QtWidgets.QAction(MainWindow)
        self.actionConnect.setObjectName("actionConnect")
        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        self.actionDisconnect.setEnabled(False)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.actionChangeServerAddress = QtWidgets.QAction(MainWindow)
        self.actionChangeServerAddress.setObjectName("actionChangeServerAddress")
        self.menuFileInfo.addAction(self.actionCreationTransactionId)
        self.menuFileInfo.addAction(self.actionLastModifiedTransactionId)
        self.menuFileInfo.addAction(self.actionCreated)
        self.menuFileInfo.addAction(self.actionLastModified)
        self.menuFileInfo.addAction(self.actionVersion)
        self.menuFileInfo.addAction(self.actionACLVersion)
        self.menuFileInfo.addAction(self.actionOwnerSessionId)
        self.menuFileInfo.addAction(self.actionDataLength)
        self.menuFileInfo.addAction(self.actionChildrenCount)
        self.menuConnect.addAction(self.actionConnect)
        self.menuConnect.addAction(self.actionDisconnect)
        self.menuConnect.addAction(self.actionChangeServerAddress)
        self.menubar.addAction(self.menuConnect.menuAction())
        self.menubar.addAction(self.menuFileInfo.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.treeWidget.setSortingEnabled(True)
        self.menuFileInfo.setTitle(_translate("MainWindow", "Node info"))
        self.menuConnect.setTitle(_translate("MainWindow", "Connection"))
        self.actionCreationTransactionId.setText(_translate("MainWindow", "Creation transaction id"))
        self.actionLastModifiedTransactionId.setText(_translate("MainWindow", "Last modified transaction id"))
        self.actionCreated.setText(_translate("MainWindow", "Created"))
        self.actionLastModified.setText(_translate("MainWindow", "Last modified"))
        self.actionVersion.setText(_translate("MainWindow", "Version"))
        self.actionACLVersion.setText(_translate("MainWindow", "ACL Version"))
        self.actionOwnerSessionId.setText(_translate("MainWindow", "Owner session id"))
        self.actionDataLength.setText(_translate("MainWindow", "Data length"))
        self.actionChildrenCount.setText(_translate("MainWindow", "Children count"))
        self.actionConnect.setText(_translate("MainWindow", "Connect"))
        self.actionDisconnect.setText(_translate("MainWindow", "Disconnect"))
        self.actionChangeServerAddress.setText(_translate("MainWindow", "Change server address"))


