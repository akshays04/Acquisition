import pymongo

client = pymongo.MongoClient("localhost", 27017)

db = client.test

db.myCollection.insert_one({"x": 10}).inserted_id