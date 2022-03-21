import socket
import threading

server_ip = 'localhost'
server_port = None
buffer_size = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command = "PlaceHolder"

def establish_control_connection(server_ip, control_server_port):
    client_socket.connect((server_ip, int(control_server_port)))
    client_socket.send(connect_request.encode('utf-8'))

connect_request = input("Enter CONNECT <server name/IP address> <server port>:")
connect_request_array = connect_request.split()
server_port = int(connect_request_array[2]) - 1
establish_control_connection(connect_request_array[1], connect_request_array[2])

#command = input("Enter your command(LIST,RETR <filename>,STOR <filename>,QUIT):")
#client_socket.send(command.encode('utf-8'))

while command.upper() != "QUIT":
    command = input("Enter your command(LIST,RETR <filename>,STOR <filename>,QUIT):")

    if command.upper() == "LIST":
        client_socket.send(command.encode('utf-8'))
        client_socket.close()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, server_port))
        server_socket.listen()
        connection_socket_server, addr = server_socket.accept()

        file_list = connection_socket_server.recv(buffer_size).decode('utf-8')
        print(file_list)

        connection_socket_server.close()
        server_socket.close()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((connect_request_array[1], int(connect_request_array[2])))

    elif "RETR" in command.upper():
        client_socket.send(command.encode('utf-8'))
        split_command_array = command.split()
        filename_retrieve = split_command_array[1]

        client_socket.close()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, server_port))
        server_socket.listen()
        connection_socket_server, addr = server_socket.accept()
        try:
            with open(str(filename_retrieve), 'wb') as f:
                chunk = connection_socket_server.recv(buffer_size)
                while chunk:
                    f.write(chunk)
                    chunk = connection_socket_server.recv(buffer_size)
        except:
            print("Not a file on server")

        connection_socket_server.close()
        server_socket.close()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((connect_request_array[1], int(connect_request_array[2])))

    elif "STOR" in command.upper():
        client_socket.send(command.encode('utf-8'))
        split_command = command.split()
        file = split_command[1]
        try:
            open_file = open(file,'rb')
            requested_file = open_file.read()
            open_file.close()
            client_socket.send(requested_file)
        except FileNotFoundError:
            print("File Not Found on Server")

        client_socket.close()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, server_port))
        server_socket.listen()
        connection_socket_server, addr = server_socket.accept()
        confirmation = connection_socket_server.recv(buffer_size).decode('utf-8')
        print(confirmation)
        
        connection_socket_server.close()
        server_socket.close()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((connect_request_array[1], int(connect_request_array[2])))

    elif command.upper() == "QUIT":
        client_socket.send(command.encode('utf-8'))
        client_socket.close()