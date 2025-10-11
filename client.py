import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 12345))

#User input
name = input("Please enter your display name: ")
client_socket.send(name.encode())


while True:
    message = input("Message: ")
    client_socket.send(message.encode())
    
    if message == "quit":
        break
    
    data = client_socket.recv(1024)
    print("Received from server:", data.decode())

client_socket.close()