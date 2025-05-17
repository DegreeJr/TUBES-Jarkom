from socket import *
import sys
import threading

HOST = ''
PORT = 1234

def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        print(f"[REQUEST from {address}]\n{request}") 

        request_line = message.splitlines()[0]
        method = request_line.split()[0]
        if method != 'GET':
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed"
            connectionSocket.sendall(response.encode())
            connectionSocket.close()
            return
        
        filename = request_line.split()[1]
        filepath = filename.lstrip('/')

        with open(filepath, 'rb') as f:
            content = f.read()

        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nConnection: close\r\n\r\n"
        connectionSocket.send(header.encode())
        connectionSocket.sendall(content)

    except FileNotFoundError:
        header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        body = "<html><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.sendall(header.encode() + body.encode())
        
    except Exception as e:
        print(f"Error: {e}")
        header = "HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\n\r\n"
        body = "<html><body><h1>500 Internal Server Error</h1></body></html>"
        connectionSocket.sendall(header.encode() + body.encode())
        
    finally:
        connectionSocket.close()

is_multithread = len(sys.argv) > 1 and sys.argv[1] == "multi"

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(5)

print(f"[STARTED] Server running on port {PORT} - Mode: {'Multi-threaded' if is_multithread else 'Single-threaded'}")

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection from {addr}")
    if is_multithread:
        thread = threading.Thread(target=handle_client, args=(connectionSocket,))
        thread.start()
    else:
        handle_client(connectionSocket,)
