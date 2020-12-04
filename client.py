import socket

HOST = '192.168.0.135' 	 # The server's hostname or IP address
PORT = 12345 		     # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostname(), 12345))
s.connect((HOST, PORT))


msg = s.recv(1024).decode("utf-8")
print(msg)

s.send(bytes("register aa 456", "utf-8"))
msg = s.recv(1024).decode("utf-8")
print(msg)

s.send(bytes("login aa 456", "utf-8"))
msg = s.recv(1024).decode("utf-8")
print(msg)

# s.send(bytes("login bb 123", "utf-8"))
# msg = s.recv(1024).decode("utf-8")
# print(msg)

# s.send(bytes("register bb 123", "utf-8"))
# msg = s.recv(1024).decode("utf-8")
# print(msg)

s.send(bytes("booking aa 0800 2", "utf-8"))		# multiple timeslots
msg = s.recv(1024).decode("utf-8")
print(msg)

s.send(bytes("leave aa 0924", "utf-8"))
msg = s.recv(1024).decode("utf-8")
print(msg)

s.send(bytes("close", "utf-8"))
msg = s.recv(1024).decode("utf-8")
print(msg)

