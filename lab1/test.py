import pymongo

client = pymongo.MongoClient("localhost", 27017)

db = client.CricStats

count = 0
for each in db.odi.find({"team1":"India"}):
    count = count + 1
    print each
print count