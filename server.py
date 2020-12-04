import socket
import pymongo

HOST = socket.gethostname()
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")		# create a client
mydb = myclient["parkingdb"]										# create a database
user = mydb["users"]												# create a new table
parking = mydb["parking_lot"]									# create a new table

client_socket, address = server.accept()
print(f"Connection from {address} has been established!")
client_socket.send(bytes("Successfully connected to the server!", "utf-8"))

while True:
	msg = client_socket.recv(1024).decode('utf-8').split()			# split message by " "

	if msg[0] == 'register':
		query = {"Username": msg[1]}
		res = user.find_one(query)
		if res != None:
			client_socket.send(bytes("The username has been used, please log in or choose another name!", "utf-8"))
		else:
			mydict = {"Username": msg[1], "Password": msg[2], "Timeslot": "null", "Number of Timeslot": "null", "Parking Location": "null"}
			user.insert_one(mydict)
			print("Create a new document:" + str(user.find_one(query)))
			client_socket.send(bytes("Sign up successfully! Your username: %s" % (msg[1]), "utf-8"))
		# continue
		

	elif msg[0] == 'login':
		query = {"Username": msg[1]}
		res = user.find(query)
		if len(list(res)) == 0:
			client_socket.send(bytes("Username or password is invalid, please check it again or sign up first!", "utf-8"))
		else:
			res = user.find(query)
			s = res.next()
			if s['Password'] != msg[2]:
				client_socket.send(bytes("Username or password is invalid, please check it again or sign up first!", "utf-8"))
			else:
				print(f"{address} has logged in!")
				client_socket.send(bytes("Successfully log in!", "utf-8"))
		# continue
		

	elif msg[0] == 'booking':
		# check if user has already booked a parking lot
		myquery = {"Username": msg[1]}
		res = user.find(myquery)
		s = res.next()
		print(s)
		if s["Timeslot"] != "null":
			client_socket.send(bytes("You have already booked a parking lot, please cancel it first!", "utf-8"))
			continue

		# check if the timeslot is valid, i.e., if the chose timeslot is not earlier than current time


		# check if there is any available parking lot for the chosen timeslot
		slot = msg[2]
		# multiple timeslots
		# for i in range(msg[3]):
		
		myquery = {msg[2]: True}
		r = parking.find(myquery)

		# if there is a parking lot available, do the following
		try:
			s = r.next()
			# update parking lot status
			newvalues = {"$set": {msg[2]: False}}			
			parking.update_one(myquery, newvalues)			# update the parking lot from "True" to "False"
			# update user's parking information
			myquery = {"Username": msg[1]}					# find the user in "user" collection
			newvalues = {"$set": {"Timeslot": msg[2], "Parking Location": s['_id']}}
			user.update_one(myquery, newvalues)				# udpate the user information
			client_socket.send(bytes("Booking successfully!", "utf-8"))
		
		# if there is no parking lot available, return error information
		except:
			client_socket.send(bytes("No parking space available for your selected time slot, please choose another one!", "utf-8"))
		

	elif msg[0] == 'leave':
		# calculate parking fee
		myquery = {"Username": msg[1]}
		r = user.find(myquery)
		s = r.next()
		init_time = s['Timeslot']
		end_time = msg[2]
		hour = int(end_time[0:2]) - int(init_time[0:2])
		minute = int(end_time[2:]) - int(init_time[2:])
		temp = "Parking time: %d:%d" % (hour, minute)
		client_socket.send(bytes(temp, "utf-8"))
		# fee = 

		# update user information
		newvalues = {"$set": {"Timeslot": "null", "Parking Location": "null"}}
		user.update_one(myquery, newvalues)
		
		# update parking lot status
		myquery = {"_id": s['Parking Location'], init_time: False}
		newvalues = {"$set": {init_time: True}}
		parking.update_one(myquery, newvalues)

		client_socket.send(bytes("Thank you for your payment!", "utf-8"))


	elif msg[0] == 'close':
		print("Bye")
		client_socket.close()
		break

server.close()