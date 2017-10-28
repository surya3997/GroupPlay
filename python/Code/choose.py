from PyQt4 import QtCore, QtGui
from list_client import Ui_List_Client        
from client import Ui_Client        
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Choose(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(355, 305)

        self.serverStatus = 0
        
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)

        self.pushButton.clicked.connect(self.clickedServer)

        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)

        self.pushButton_2.clicked.connect(self.clickedClient)

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Group Play", None))
        self.pushButton.setText(_translate("Form", "Play song", None))
        self.pushButton_2.setText(_translate("Form", "Listen", None))

    def clickedServer(self):
        if self.serverStatus == 0:
            self.server = QtGui.QWidget()
            self.server_ui = Ui_List_Client()
            self.server_ui.setupUi(self.server)
            self.serverStatus = 1
            self.server.show()
        else:
            print("No")

    def clickedClient(self):
        if self.serverStatus == 1:
            # self.server.close()
            sys.exit()
        self.client = QtGui.QWidget()
        self.client_ui = Ui_Client()
        self.client_ui.setupUi(self.client)
        self.client.show()



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Choose()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

