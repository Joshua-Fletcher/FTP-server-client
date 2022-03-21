import socket
import threading
import os
import pathlib


server_ip = 'localhost'
control_port = 3200
buffer_size = 1024

client_server_port = None

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, control_port))
server_socket.listen()

def handle_request(connection_socket):
    command = "PlaceHolder"
    while(command.upper() != "QUIT"):
        command = connection_socket.recv(buffer_size).decode('utf-8')
        print(command)

        if command.upper() == "QUIT":
            connection_socket.close()
            server_socket.close()

        elif "CONNECT" in command.upper():
            connect_request_array = command.split() 
            client_server_port = int(connect_request_array[2]) - 1
            print(client_server_port)

        elif command.upper() == "LIST":
            connection_socket.close()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, 3199))
            file_list = str(os.listdir('.'))
            client_socket.send(file_list.encode('utf-8'))
            client_socket.close()

            server_socket.listen()
            connection_socket, addr = server_socket.accept()

        elif "RETR" in command.upper():
            connection_socket.close()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, 3199))
            split_command = command.split()
            file = split_command[1]
            try:
                open_file = open(file,'rb')
                requested_file = open_file.read()
                open_file.close()
                client_socket.send(requested_file)
            except FileNotFoundError:
                error_message = "File Not Found on Server"
                client_socket.send(error_message.encode('utf-8'))
        
            client_socket.close()

            server_socket.listen()
            connection_socket, addr = server_socket.accept()

        elif "STOR" in command.upper():
            split_command = command.split()
            file_name = split_command[1]
            
            try:
                with open(str(file_name), 'wb') as f:
                    chunk = connection_socket.recv(buffer_size)
                    while chunk:
                        f.write(chunk)
                        chunk = connection_socket.recv(buffer_size)
            except:
                print("ERROR")

            connection_socket.close()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, 3199))
            confirmation_message = "File is uploaded on Server"
            client_socket.send(confirmation_message.encode('utf-8'))

            client_socket.close()

            server_socket.listen()
            connection_socket, addr = server_socket.accept()

    connection_socket.close()
    server_socket.close()

while True:
    connection_socket, addr = server_socket.accept()
    threading.Thread(target=handle_request, args=(connection_socket,)).start()
    server_socket.close()