import socket
import time
import threading

path = "/media/surya/Entertainment/Songs/Collection/Indian/Telephone Manipol.mp3"

with open(path, 'rb') as f:
    text = f.read()

print(len(text))

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        self.host1 = host
        self.port1 = 3998
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock1.bind((self.host1, self.port1))

        self.listeners = []
        self.flagPort = []

    def listen(self):
        self.sock.listen(5)
        self.sock1.listen(5)
        self.stopScan = 1
        threading.Thread(target = self.seek).start()
        while self.stopScan:
            client, address = self.sock.accept()
            client1, address1 = self.sock1.accept()
            client.settimeout(160)
            client1.settimeout(160)
            clientListener = threading.Thread(target = self.listenToClient,args = (client,address))
            clientListener.daemon = True
            clientListener.start()
            flagListener = threading.Thread(target = self.listenForFlag,args = (client1,address1))
            flagListener.daemon = True
            flagListener.start()
            self.listeners.append(client)
            self.flagPort.append(client1)

    def seek(self):
        s = 0
        self.check = 0
        checkerUp = threading.Thread(target=self.checkUpdate)
        checkerUp.daemon = True
        checkerUp.start()
        while True:
            s = input("percent : ")
            self.stopScan = 0
            self.check += 1
            self.check = self.check % 10
            # print(self.check)
            self.chunk = text[int((int(s) / 100) * len(text)):]
            print(len(self.chunk))
            for c in self.listeners:
                c.sendall(self.chunk)


    def checkUpdate(self):
        while True:
            for fc in self.flagPort:
                # print(self.check)
                time.sleep(1)
                fc.send(str(self.check).encode())

    def listenToClient(self, client, address):
        print(str(address[0]) + ' : ' + str(address[1]), "connected")
        while True:
            connection = client.recv(10)
            if not connection:
                print(str(address[0]) + ' : ' + str(address[1]), "disconnected") 
                self.listeners.remove(client)
                break

    def listenForFlag(self, client, address):
        while True:
            connection = client.recv(10)
            # client.send(str(self.check).encode())
            if not connection:
                self.flagPort.remove(client)
                break

        

if __name__ == "__main__":
    port_num = 3997
    ThreadedServer('',port_num).listen()
