from PyQt4 import QtCore, QtGui
from list_songs import Ui_Songs
from player import Ui_Player
import sys, os, socket, threading

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

host = '0.0.0.0'
msgPort = 3997

# class ThreadedMsgServer(object):
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.sock.bind((self.host, self.port))

#     def listen(self):
#         self.sock.listen(5)
#         self.stopScan = 1
#         self.listeners = []
#         while self.stopScan:
#             client, address = self.sock.accept()
#             self.listeners.append(client)
#             client.settimeout(160)
#             clientListener = threading.Thread(target = self.listenToClient,args = (client,address))
#             clientListener.daemon = True
#             clientListener.start()
#             s = input("stop? ")
#             if s == "yes":
#                 self.stopScan = False

#         statusToClient = threading.Thread(target=self.sendStatus)
#         statusToClient.daemon = True
#         statusToClient.start()
#     def listenToClient(self, client, address):
#             print(str(address[0]) + ' : ' + str(address[1]), "connected")
            
#             while True:
#                 connection = client.recv(1024)
#                 if not connection:
#                     print(str(address[0]) + ' : ' + str(address[1]), "disconnected") 
#                     break
                        

#     def sendStatus(self):
#         while True:
#             reply = input("Enter status : ")
#             reply += ' '
#             for i in self.listeners:
#                 sendReply = reply.encode(encoding='UTF-8')
#                 #print(sendReply)
#                 i.send(sendReply)


class Ui_List_Client(object):
    stopServer = 1
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(353, 300)

        self.noClients = 0

        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 7, 0, 1, 1)

        self.pushButton.clicked.connect(lambda: self.stopServer(Form))

        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 6, 0, 1, 1)

        self.pushButton_3.clicked.connect(lambda: self.clickedSongs(Form))

        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))

        self.gridLayout.addWidget(self.listWidget, 5, 0, 1, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Form)
        msgServHand = threading.Thread(target=self.messageServerHandler)
        msgServHand.daemon = True
        msgServHand.start()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def messageServerHandler(self):
        self.host = host
        self.port = msgPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        self.sock.listen(5)
        self.stopScan = 1
        self.listeners = []
        while self.stopServer and Ui_Songs.stopServer and Ui_Player.stopServer:
            client, address = self.sock.accept()
            self.listeners.append(client)
            # client.settimeout(160)
            clientListener = threading.Thread(target = self.listenToClient,args = (client,address))
            clientListener.daemon = True
            clientListener.start()
        print("server stopped listening!")

    def listenToClient(self, client, address):
        listItem = QtGui.QListWidgetItem()
        self.listWidget.addItem(listItem)
        itemNo = self.noClients
        self.noClients += 1
        item = self.listWidget.item(itemNo)
        item.setText(_translate("Form", str(address[0]) + ' : ' + str(address[1]), None))

        # print(str(address[0]) + ' : ' + str(address[1]), "connected")
        while True:
            connection = client.recv(1024)
            if not connection:
                # print(str(address[0]) + ' : ' + str(address[1]), "disconnected") 
                item = self.listWidget.item(itemNo)
                item.setText(_translate("Form", "Disconnected", None))
                self.listeners.remove(client)
                break

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Listeners", None))
        self.pushButton.setText(_translate("Form", "Back", None))
        self.pushButton_3.setText(_translate("Form", "Proceed", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)

        # item = self.listWidget.item(0)
        # item.setText(_translate("Form", "New Item", None))

        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\">Listeners</p></body></html>", None))

    def stopServer(self, Form):
        self.stopServer = False
        self.sock.close()
        Form.close()

    def clickedSongs(self, Form):
        self.songWidget = QtGui.QWidget()
        self.songs_ui = Ui_Songs()
        self.songs_ui.setupUi(self.songWidget, self.listeners)
        Form.close()
        self.sock.close()
        self.songWidget.show()
        


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_List_Client()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

