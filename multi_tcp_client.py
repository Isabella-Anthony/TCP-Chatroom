import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(('localhost', 12345))
        print("Connected to server!")
        
        # Receive welcome message
        welcome = client.recv(1024).decode()
        print(welcome, end='')
        
        # Send name
        name = input()
        client.send(name.encode())
        
        # Receive greeting
        greeting = client.recv(1024).decode()
        print(greeting)
        
        # Main loop for sending expressions
        while True:
            # Get user input
            expression = input("Expression: ")
            client.send(expression.encode())
            
            # Check if user wants to quit
            if expression.lower() == 'quit':
                goodbye = client.recv(1024).decode()
                print(goodbye)
                break
            
            # Receive result
            result = client.recv(1024).decode()
            print(result)
            
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()