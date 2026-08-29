import socket
from TLS import TLS_client

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 2000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST,PORT))
    protected_socket = TLS_client(client)
    protected_socket.handshake_client()

#https://realpython.com/python-sockets/ - used this to help with understanding how to use the socket module