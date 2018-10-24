from PyQt5 import QtCore, QtWidgets
from list_client import Ui_List_Client        
from client import Ui_Client        
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_Choose(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(355, 305)

        self.serverStatus = 0
        
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)

        self.pushButton.clicked.connect(self.clickedServer)

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)

        self.pushButton_2.clicked.connect(self.clickedClient)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Group Play", None))
        self.pushButton.setText(_translate("Form", "Play song", None))
        self.pushButton_2.setText(_translate("Form", "Listen", None))

    def clickedServer(self):
        if self.serverStatus == 0:
            self.server_widget = QtWidgets.QWidget()
            self.server_ui = Ui_List_Client()
            self.server_ui.setupUi(self.server_widget)
            self.server_widget.show()
        else:
            print("No")

    def clickedClient(self):
        if self.serverStatus == 1:
            sys.exit()
        self.client = QtWidgets.QWidget()
        self.client_ui = Ui_Client()
        self.client_ui.setupUi(self.client)
        self.client.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Choose()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

