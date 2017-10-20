import socket
import threading

path = "./Thalli.mp3"

with open(path, 'rb') as f:
    text = f.read()

print(len(text))

##part1 = text[:int(len(text) / 2)]
##part2 = text[int(len(text) / 2):]

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(160)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        print("connected...")
        
##        try:
##        print(text[20000])
        client.send(text)
##        except:
##            print("no expect")
##            client.close()
##            return False

##        while True:
##            pass

if __name__ == "__main__":
    port_num = 3997
    ThreadedServer('',port_num).listen()
