#code used for starting the server

import socket
from TLS import TLS_server

HOST = "127.0.0.1" #localhost
PORT = 2000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST,PORT))
    server.listen()
    connection, address = server.accept() #accepts connections - creates connection object
    secure_connection = TLS_server(connection)
    secure_connection.handshake_server()

#https://realpython.com/python-sockets/ - used this to help with understanding how to use the socket module