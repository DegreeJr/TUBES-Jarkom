from socket import *
import sys

if len(sys.argv) != 4:
    print("Penggunaan: python client.py <server_host> <server_port> <filename>")
    sys.exit()

server_host = sys.argv[1]
server_port = int(sys.argv[2])
filename = sys.argv[3]

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((server_host, server_port))

message = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
clientSocket.send(request.encode())

response = b""
while True:
    data = clientSocket.recv(4096)
    if not data:
        break
    response += data

print("=== Response ===")
print(response.decode(errors="ignore"))
