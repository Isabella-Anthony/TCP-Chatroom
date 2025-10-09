import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 12345))

server_socket.listen(1)
print("TCP server is listening...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")
name = conn.recv(1024).decode()
print("entered chats:", name)

while True:
      
    data = conn.recv(1024).decode()

    if data == "quit":
        break  
    
    print("Received:", data)
    conn.send(data.upper().encode())

conn.close()