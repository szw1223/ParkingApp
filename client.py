import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostname(), 12345))
s.connect((HOST, PORT))


while True:
	msg = s.recv(50).decode("utf-8")
	print(msg)

	s.send(bytes("database", "utf-8"))

	s.send(bytes("close", "utf-8"))
	break