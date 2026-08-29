import socket

class TLS_client(socket.socket):

    def __init__(self,raw_tcp_socket):

        self.protected_socket = raw_tcp_socket

    def handshake_client(self):
        send_data(self.protected_socket,b"hello")

class TLS_server(socket.socket):

    def __init__(self,raw_tcp_socket):

        self.protected_socket = raw_tcp_socket

    def handshake_server(self):

        self.protected_socket.listen()
        conn, addr = self.protected_socket.accept()

        payload = recieve_data(conn)
        print(payload)

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


    