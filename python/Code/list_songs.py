from PyQt5 import QtCore, QtWidgets
from player import Ui_Player
import os

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

class Ui_Songs(object):
    stopServer = 1
    def setupUi(self, Form, listeners):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(353, 300)
        self.listeners = listeners
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 7, 0, 1, 1)

        self.pushButton.clicked.connect(lambda: self.stopSongsUi(Form))

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 6, 0, 1, 1)

        self.pushButton_3.clicked.connect(lambda: self.clickedPlayer(Form))

        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))

        self.gridLayout.addWidget(self.listWidget, 5, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Songs", None))
        self.pushButton.setText(_translate("Form", "Back", None))
        self.pushButton_3.setText(_translate("Form", "Proceed", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)

        path1 = "./"
        x = [(i[0],i[2]) for i in os.walk(path1)]
        self.name = []
        self.fullPath = []
        self.noSongs = 0
        for t in x:
            for f in t[1]:
                if f[-3:] == 'mp3' or f[-3:] == 'MP3':
                    self.name.append(f)
                    self.fullPath.append(t[0] + '/' + f)

                    itemList = QtWidgets.QListWidgetItem()
                    self.listWidget.addItem(itemList)
                    item = self.listWidget.item(self.noSongs)
                    self.noSongs += 1
                    item.setText(_translate("Form", f, None))

        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\">Choose song to stream</p></body></html>", None))

    def stopSongsUi(self, Form):
        self.stopServer = False
        Form.close()

    def clickedPlayer(self, Form):
        print(self.listWidget.currentRow())
        print(self.listWidget.currentItem().text())
        self.playerWidget = QtWidgets.QWidget()
        self.player_ui = Ui_Player()
        self.player_ui.setupUi(self.playerWidget, self.listWidget.currentRow(), self.fullPath, self.name, self.listeners)
        Form.close()
        self.playerWidget.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Songs()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

