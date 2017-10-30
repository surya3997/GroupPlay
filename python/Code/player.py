from PyQt4 import QtCore, QtGui
import threading, vlc, time
from shutil import copyfile

import sys, os, socket
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer

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




''' 
message - 3997
http - 8080

'''

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

class Ui_Player(object):
    stopServer = 1
    def setupUi(self, Form, rowIndex, fullPathList, songNameList, listeners):
        self.playStatus = 1
        self.rowIndex = rowIndex
        self.fullPathList = fullPathList
        self.songNameList = songNameList
        self.listeners = listeners

        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(648, 380)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 6, 0, 1, 1)

        self.pushButton.clicked.connect(lambda: self.stopPlayer(Form))

        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.horizontalSlider = QtGui.QSlider(Form)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.verticalLayout.addWidget(self.horizontalSlider)

        self.horizontalSlider.sliderReleased.connect(self.seek)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_5 = QtGui.QPushButton(Form)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.pushButton_6 = QtGui.QPushButton(Form)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout.addWidget(self.pushButton_6)
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_7 = QtGui.QPushButton(Form)
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.horizontalLayout.addWidget(self.pushButton_7)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))

        self.gridLayout.addWidget(self.listWidget, 2, 0, 1, 1)

        threading.Thread(target=self.startHTTPServer).start()
        self.retranslateUi(Form)
        self.vlcPlay.play()
        self.sendStatus("play 0")
        QtCore.QMetaObject.connectSlotsByName(Form)

    def startHTTPServer(self):
        HOST = socket.gethostname()
        PORT = 8080
        CWD = os.getcwd()
        server = ThreadingSimpleServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
        print("Serving HTTP traffic from", CWD, "on", HOST, "using port", PORT)
        try:
            while 1:
                sys.stdout.flush()
                server.handle_request()
        except KeyboardInterrupt:
            print("\nShutting down server per users request.")

    def printPosition(self):
        print(self.horizontalSlider.value())

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Player", None))
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\">Playing your tune!!! :)</p></body></html>", None))
        self.pushButton.setText(_translate("Form", "Back", None))
        self.pushButton_4.setText(_translate("Form", "<<", None))
        self.pushButton_5.setText(_translate("Form", "<", None))
        self.pushButton_6.setText(_translate("Form", "|> / ||", None))
        self.pushButton_2.setText(_translate("Form", ">", None))
        self.pushButton_7.setText(_translate("Form", ">>", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)

        for index, itemName in enumerate(self.songNameList):
            itemList = QtGui.QListWidgetItem()
            self.listWidget.addItem(itemList)
            item = self.listWidget.item(index)
            item.setText(_translate("Form", itemName, None))

        self.pushButton_6.clicked.connect(self.playSong)
        self.copySong()
        time.sleep(2)
        self.vlcPlay = vlc.MediaPlayer("./song.mp3")

        self.pushButton_2.clicked.connect(self.forward)
        self.pushButton_5.clicked.connect(self.backward)
        self.pushButton_7.clicked.connect(self.next)
        self.pushButton_4.clicked.connect(self.previous)

        self.listWidget.setSortingEnabled(__sortingEnabled)
    
    def copySong(self):
        copyfile(self.fullPathList[self.rowIndex], './song.mp3')
        time.sleep(2)

    def stopPlayer(self, Form):
        self.stopServer = False
        Form.close()

    def sendStatus(self, toSend):
        reply = toSend
        reply += ' '
        for i in self.listeners:
            sendReply = reply.encode(encoding='UTF-8')
            #print(sendReply)
            i.send(sendReply)

    def playSong(self):
        if self.playStatus == 0:
            self.vlcPlay.play()
            self.playStatus = 1
            self.sendStatus("play 1")
            # while True:
            #     time.sleep(1)
            #     self.horizontalSlider.setValue(round(self.vlcPlay.get_position() * 100))
        else:
            self.vlcPlay.pause()
            self.sendStatus("paus")
            self.playStatus = 0

    def forward(self):
        self.sendStatus("fwrd 1")
        self.vlcPlay.set_position(self.vlcPlay.get_position() + 0.01)

    def backward(self):
        self.sendStatus("bwrd 1")
        self.vlcPlay.set_position(self.vlcPlay.get_position() - 0.01)

    def next(self):
        if self.rowIndex < len(self.fullPathList) - 1:
            self.rowIndex += 1
            self.vlcPlay.stop()
            self.playStatus = 0
            self.copySong()
            self.sendStatus("paus")
            time.sleep(1)
            self.sendStatus("play 0")
            time.sleep(1)
            self.vlcPlay = vlc.MediaPlayer("./song.mp3")
            self.vlcPlay.play()
            self.playStatus = 1

    def previous(self):
        if self.rowIndex > 0:
            self.rowIndex -= 1
            self.vlcPlay.stop()
            self.playStatus = 0
            self.copySong()
            self.sendStatus("paus")
            time.sleep(1)
            self.sendStatus("play 0")
            time.sleep(1)
            self.vlcPlay = vlc.MediaPlayer("./song.mp3")
            self.vlcPlay.play()
            self.playStatus = 1

    def seek(self):
        value = self.horizontalSlider.value()
        self.sendStatus("seek " + str(value))
        self.vlcPlay.set_position(value / 100)
        

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Player()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

