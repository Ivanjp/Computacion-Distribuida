import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', int(sys.argv[1]))
sock.connect(server_address)
sock.sendall(("@p2p P ag palabra significado").encode())
print(sock.recv(1024).decode("utf-8"))
sock.sendall(("@p2p P ag palabra2 significado2").encode())
print(sock.recv(1024).decode("utf-8"))