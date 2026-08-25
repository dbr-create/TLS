import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 2000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT)) #Connects to Server with specified (HOST,PORT)
    client.sendall(b"Hello, world")
    data = client.recv(1024)

print(f"Received {data!r}")

#https://realpython.com/python-sockets/ - used this to help with understanding how to use the socket module