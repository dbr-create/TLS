import socket

class TLS_client(socket.socket):
    def __init__(self,raw_tcp_socket):
        self.protected_socket = raw_tcp_socket
    def handshake_client(self):
        return

class TLS_server(socket.socket):
    def __init__(self,raw_tcp_socket):
        self.protected_socket = raw_tcp_socket
    def handshake_client(self):
        return