import socket
import threading
import ast
import operator

# Safe operations whitelist
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

SAFE_FUNCTIONS = {
    'abs': abs,
    'min': min,
    'max': max,
    'round': round,
    'sum': sum,
    'len': len,
}

def safe_eval(expression, max_length=200):
    """Safely evaluate mathematical expressions using AST parsing"""
    
    if len(expression) > max_length:
        return "Error: Expression too long"
    
    if not expression.strip():
        return "Error: Empty expression"
    
    try:
        node = ast.parse(expression, mode='eval').body
        return str(_eval_node(node))
    except SyntaxError:
        return "Error: Invalid syntax"
    except Exception as e:
        return f"Error: {type(e).__name__}"

def _eval_node(node):
    """Recursively evaluate AST nodes with whitelist checking"""
    
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float, complex)):
            return node.value
        raise ValueError("Only numeric constants allowed")
    
    if isinstance(node, ast.BinOp):
        if type(node.op) not in SAFE_OPERATORS:
            raise ValueError(f"Operation {type(node.op).__name__} not allowed")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return SAFE_OPERATORS[type(node.op)](left, right)
    
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in SAFE_OPERATORS:
            raise ValueError(f"Operation {type(node.op).__name__} not allowed")
        operand = _eval_node(node.operand)
        return SAFE_OPERATORS[type(node.op)](operand)
    
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls allowed")
        
        func_name = node.func.id
        if func_name not in SAFE_FUNCTIONS:
            raise ValueError(f"Function '{func_name}' not allowed")
        
        args = [_eval_node(arg) for arg in node.args]
        return SAFE_FUNCTIONS[func_name](args) if func_name in ['min', 'max', 'sum'] else SAFE_FUNCTIONS[func_name](*args)
    
    if isinstance(node, ast.List):
        return [_eval_node(elem) for elem in node.elts]
    
    raise ValueError(f"Node type {type(node).__name__} not allowed")

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    client_name = "Unknown"
    
    try:
        # Send welcome message
        conn.send("Welcome! Please enter your name: ".encode())
        
        # Receive client name
        name_data = conn.recv(1024)
        if name_data:
            client_name = name_data.decode().strip()
            print(f"Client identified as: {client_name} from {addr}")
            conn.send(f"Hello {client_name}! You can now send expressions (type 'quit' to exit).\n".encode())
        
        # Handle expressions
        while True:
            data = conn.recv(1024)
            
            if not data:
                print(f"[{client_name}] disconnected")
                break
            
            expression = data.decode().strip()
            
            # Check for quit command
            if expression.lower() == 'quit':
                print(f"[{client_name}] requested to quit")
                conn.send("Goodbye!\n".encode())
                break
            
            # Print expression on server side
            print(f"[{client_name}] Expression: {expression}")
            
            result = safe_eval(expression)
            print(f"[{client_name}] Result: {result}")
            response = f"Result: {result}\n"
            conn.send(response.encode())
            
    except Exception as e:
        print(f"Error handling client {client_name} ({addr}): {e}")
    finally:
        conn.close()
        print(f"Connection with {client_name} ({addr}) closed.\n")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()
    print("=" * 50)
    print("Server listening on port 12345...")
    print("Waiting for clients...")
    print("=" * 50 + "\n")

    try:
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()