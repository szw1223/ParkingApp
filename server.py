import socket
import pymongo

HOST = '127.0.0.1'
PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((socket.gethostname(), 12345))
s.bind((HOST, PORT))
s.listen(5)

while True:
	client_socket, address = s.accept()
	print(f"Connection from {address} has been established!")
	client_socket.send(bytes("Welcome to the server!", "utf-8"))

	if client_socket.recv(50).decode('utf-8') == 'database':
		myclient = pymongo.MongoClient("mongodb://localhost:27017/")
		mydb = myclient["mydatabase"]
		mycol = mydb["customers"]
		mydict = [
			{"_id": 1, "name": "John", "address": "Highway 37"},
			{"_id": 2, "name": "Peter", "address": "Lowstreet 27"}
		]

		x = mycol.insert_many(mydict)
		print("The database has been established!")
	
	if client_socket.recv(50).decode('utf-8') == 'close':
		print(f"Bye")
		client_socket.close()
		break

s.close()