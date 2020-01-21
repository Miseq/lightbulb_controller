import requests
import http.server as server
import socket
import socketserver


class LightBulb:
    def __init__(self, port=8080):
        self.status = 0
        self.port = port  #tylko port, w zadaniu host zawsze będzie 'localhost'

    def turn_on(self):
        self.status = 1

    def turn_off(self):
        self.status = 0

    def get_status(self):
        return self.status

    def check_port_aviability(self):
        is_port_open = False
        while is_port_open == False:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.bind(('localhost', self.port))
                    is_port_open = True
                except:
                    self.port += 1
            sock.close()
        print(f"device will listen on port {self.port}")

    def start_server(self):
        self.check_port_aviability()
        Handler = server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("127.0.0.1", self.port), Handler) as httpd:
            print(f"Device started, listening at port {self.port}")
            httpd.serve_forever()


w = LightBulb()
w.start_server()