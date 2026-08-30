#TLS classes for client and server

import socket
import os

class TLS_client(socket.socket):

    def __init__(self,raw_tcp_socket):

        self.protected_socket = raw_tcp_socket

    def handshake_client(self):

        #client nonce
        nonce = os.urandom(16)

        #client sending client hello - nonce
        send_data(self.protected_socket,nonce)

        server_hello = recieve_data(self.protected_socket)

        print(server_hello)

class TLS_server(socket.socket):

    def __init__(self,raw_tcp_socket):

        self.protected_socket = raw_tcp_socket

    def handshake_server(self):

        #server nonce
        nonce = os.urandom(16)

        #server recieving client hello
        client_hello = recieve_data(self.protected_socket)

        print(client_hello)

        #server sending server hello - nonce
        server_hello = send_data(self.protected_socket,nonce)

#functions to handle the fact that TCP transmits as a stream (i.e. headers needed to seperate different messages - Clienthello,DH exchange etc.)
def send_data(socket,payload):

    payload_length = len(payload)
    
    header = payload_length.to_bytes(4, byteorder='big') #4 byte header (allows up to 2^32 bit length message - i.e. 2^8 bytes)

    socket.sendall(header + payload)

def recieve_data(socket):

    header = b""

    #Handles recieving 4 byte header
    while len(header) < 4: 

        chunk = socket.recv(4 - len(header))

        if not chunk:

            raise ConnectionError("Connection timed out while reading header")

        header += chunk

    payload_length = int.from_bytes(header, byteorder='big')

    payload = b""

    #Handles recieving actual payload
    while len(payload) < payload_length:

        chunk = socket.recv(payload_length - len(payload))

        if not chunk:

            raise ConnectionError("Connection timed out while reading payload")

        payload += chunk

    return payload


    