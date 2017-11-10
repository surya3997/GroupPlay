from PyQt4 import QtCore, QtGui
import vlc
import socket, time

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

class Ui_Client(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(354, 300)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_2 = QtGui.QLineEdit(Form)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)

        self.pushButton.clicked.connect(lambda: self.stopClient(Form))

        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)

        self.retranslateUi(Form)

        self.pushButton_2.clicked.connect(self.connectToIP)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def connectToIP(self):
        ip = self.lineEdit_2.text()
        portsn=8080
        portms=3997
        ser_add=(ip,portms)

        sock=socket.socket()
        flag = 0
        try:
            sock.connect(ser_add)
            flag = 1
        except:
            print("Server not ready!")

        if flag == 1:
            songname="song.mp3"
            loc="http://"+ip+":"+str(portsn)+"/"+songname
            req=sock.recv(1024);
            songname="song.mp3"
            a=req.decode()
            print(a)
            if a:
                if(a[0:4]=="play"):
                    p = vlc.MediaPlayer(loc)
                    a=a.split();
                    pos=float(a[1])
                    p.set_position(pos)
                    self.setStatusMsg("Playing...")
                    p.play()
                while(True):
                    req=sock.recv(1024);
                    a=req.decode()
                    print(a)
                    if a:
                        if(a[0:4]=="play"):
                            a=a.split();
                            if(a[1]=="0"):
                                p.stop()
                                time.sleep(2)
                                p = vlc.MediaPlayer(loc)
                                self.setStatusMsg("Playing...")
                                p.play()
                            else:
                                self.setStatusMsg("Playing...")
                                p.play()
                        elif(a[0:4]=="paus"):
                            self.setStatusMsg("Paused...")
                            p.pause()

                        elif(a[0:4]=="fwrd"):
                            po=p.get_position();
                            p.stop()
                            p = vlc.MediaPlayer(loc)
                            p.play()
                            p.set_position(po+0.01)        
                        elif(a[0:4]=="bwrd"):
                            po=p.get_position();
                            p.stop()
                            p = vlc.MediaPlayer(loc)
                            p.play()
                            p.set_position(po-0.01)
                        elif(a[0:4]=="seek"):
                            a=a.split()
                            po=p.get_position();
                            po=int(a[1])/100
                            p.stop()
                            p = vlc.MediaPlayer(loc)
                            p.play()
                            p.set_position(po)
                    else:
                        break

    def stopClient(self, Form):
        Form.close()

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Listening", None))
        self.pushButton_2.setText(_translate("Form", "IP", None))
        self.pushButton.setText(_translate("Form", "Back", None))
        self.setStatusMsg("STATUS")

    def setStatusMsg(self, msg):
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">" + msg + "</span></p></body></html>", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Client()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

