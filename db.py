import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")		# create a client
mydb = myclient["parkingdb"]										# create a database
user = mydb["users"]												# create a new collection
parking = mydb["parking_lot"]									# create a new collection

user.drop()
parking.drop()


mydict = [
	{"_id": 1, "0800": True, "0900": True, "1000": True},
	{"_id": 2, "0800": True, "0900": True, "1000": True}
]

parking.insert_many(mydict)