import sys, os, socket
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socket
import threading

HOST = socket.gethostname()

''' 
message - 3997
http - 8080

'''

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

'''
This sets the listening port, default port 8080
'''
if sys.argv[1:]:
    PORT = int(sys.argv[1])
else:
    PORT = 8080

'''
This sets the working directory of the HTTPServer, defaults to directory where script is executed.
'''
if sys.argv[2:]:
    os.chdir(sys.argv[2])
    CWD = sys.argv[2]
else:
    CWD = os.getcwd()


def startHTTPServer():
    server = ThreadingSimpleServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
    print("Serving HTTP traffic from", CWD, "on", HOST, "using port", PORT)
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print("\nShutting down server per users request.")

httpStart = threading.Thread(target = startHTTPServer).start()


msgPort = 3997

class ThreadedMsgServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        self.stopScan = 1
        self.listeners = []
        while self.stopScan:
            client, address = self.sock.accept()
            self.listeners.append(client)
            client.settimeout(160)
            clientListener = threading.Thread(target = self.listenToClient,args = (client,address))
            clientListener.daemon = True
            clientListener.start()
            s = input("stop? ")
            if s == "yes":
                self.stopScan = False

        statusToClient = threading.Thread(target=self.sendStatus)
        statusToClient.daemon = True
        statusToClient.start()
    def listenToClient(self, client, address):
            print(str(address[0]) + ' : ' + str(address[1]), "connected")
            
            while True:
                connection = client.recv(1024)
                if not connection:
                    print(str(address[0]) + ' : ' + str(address[1]), "disconnected") 
                    break
                        

    def sendStatus(self):
        while True:
            reply = input("Enter status : ")
            reply += ' '
            for i in self.listeners:
                sendReply = reply.encode(encoding='UTF-8')
                #print(sendReply)
                i.send(sendReply)

msgServer = ThreadedMsgServer('0.0.0.0', msgPort)
msgServer.listen()