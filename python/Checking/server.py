import socket
import threading

path = "./Thalli.mp3"

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
        threading.Thread(target = self.seek).start()
        while True:
            client, address = self.sock.accept()
            client1, address1 = self.sock.accept()
            client.settimeout(160)
            client1.settimeout(160)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()
            threading.Thread(target = self.listenForFlag,args = (client1,address1)).start()
            self.listeners.append(client)
            self.flagPort.append(client)

    def seek(self):
        s = 0
        while True:
            self.chunk = text[int((int(s) / 100) * len(text)):]
            for c in self.listeners:
                c.send(self.chunk)

            s = input("percent : ")
            check += 1
            for fc in self.flagPort:
                fc.send(str(check).encode())

    def listenToClient(self, client, address):
        size = 1024
        print(str(address[0]) + ' : ' + str(address[1]), "connected")
        while True:
            connection = client.recv(10)
            conn = connection.decode()
            if not conn:
                print(str(address[0]) + ' : ' + str(address[1]), "disconnected") 
                self.listeners.remove(client)

    def listenForFlag(self, client, address):
        while True:
            connection = client.recv(10)
            conn = connection.decode()
            if not conn:
                self.flagPort.remove(client)

        

if __name__ == "__main__":
    port_num = 3997
    ThreadedServer('',port_num).listen()
