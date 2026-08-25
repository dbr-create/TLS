import socket

HOST = "127.0.0.1" #localhost
PORT = 2000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST,PORT))
    server.listen()
    connection, address = server.accept() #accepts connections - creates connection object

    while True:
        data = connection.recv(1024) #Allows for recieving data, argument 1024 specifies buffer size
        if not data:
            break
        connection.sendall(data) #sends data back

#https://realpython.com/python-sockets/ - used this to help with understanding how to use the socket module