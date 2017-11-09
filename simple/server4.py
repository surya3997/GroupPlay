import http.server
import threading

class Server(threading.Thread):
    def __init__(self, port, address):
        HandlerClass = BlogofileRequestHandler
        ServerClass = http.server.HTTPServer
        self.httpd = ServerClass(('127.0.0.1', 8080), HandlerClass)

    def run(self):
        self.httpd.serve_forever()

    def shutdown(self):
        self.httpd.shutdown()
        self.httpd.socket.close()

class BlogofileRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        http.server.SimpleHTTPRequestHandler.__init__(
            self, *args, **kwargs)

    def translate_path(self, path):
        ...