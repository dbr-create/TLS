#TLS classes for client and server

import socket
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, ParameterFormat, load_pem_public_key, load_pem_parameters
from EDH import generate_parameters, generate_key_pair, establish_shared_key

class TLS_client(socket.socket):

    def __init__(self,raw_tcp_socket):

        self.protected_socket = raw_tcp_socket

    def handshake_client(self):

        #client sending client hello - to be replaced with cipher suite at a later date
        #No negotiation of TLS version (assumed 1.2 using EDH)
        send_data(self.protected_socket,b'hello')

        #server hello
        encoded_parameters = recieve_data(self.protected_socket)

        parameters = load_pem_parameters(encoded_parameters)

        private_key, public_key = generate_key_pair(parameters)

        encoded_public_key = public_key.public_bytes(Encoding.PEM,PublicFormat.SubjectPublicKeyInfo)

        send_data(self.protected_socket,encoded_public_key)

        peer_public_key = load_pem_public_key(recieve_data(self.protected_socket))

        shared_key = establish_shared_key(private_key,peer_public_key)

        print(shared_key)

class TLS_server(socket.socket):

    def __init__(self,raw_tcp_socket):

        self.protected_socket = raw_tcp_socket

    def handshake_server(self):

        #server recieving client hello
        client_hello = recieve_data(self.protected_socket)

        print(client_hello)

        parameters = generate_parameters()

        encoded_parameters = parameters.parameter_bytes(Encoding.PEM,ParameterFormat.PKCS3)

        send_data(self.protected_socket,encoded_parameters)

        private_key, public_key = generate_key_pair(parameters)

        encoded_public_key = public_key.public_bytes(Encoding.PEM,PublicFormat.SubjectPublicKeyInfo)

        #server sending server hello - EDH public key
        send_data(self.protected_socket,encoded_public_key)

        peer_public_key = load_pem_public_key(recieve_data(self.protected_socket))

        shared_key = establish_shared_key(private_key,peer_public_key)

        print(shared_key)

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

#used https://www.ibm.com/docs/en/sdk-java-technology/8?topic=handshake-tls-12-protocol for pseudocode on the steps of TLS (1.2)
#used https://cryptography.io/en/3.4.2/hazmat/primitives/asymmetric/serialization.html for information on how to convert a key/paramaters objects into byte format (specifically went with PEM)
#used https://stackoverflow.com/questions/77288976/how-to-export-a-private-key-public-key-into-bytes-with-python-cryptography-mod for an example of the byte conversion used in actual code

    