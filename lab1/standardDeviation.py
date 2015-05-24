import pymongo
import math

client = pymongo.MongoClient("localhost", 27017)
db = client.CricStats
count = 0
sum=0
for each in db.odi.find({ 'location': { '$in': ['Adelaide' ] } }):
    sum=sum+int(each.get('team1 Total'))
    count=count+1    
team1AvgScore=math.ceil(sum/count)

count = 0
sum=0
for each in db.odi.find({ 'location': { '$in': ['Adelaide' ] } }):
    if (each.get('team1')=='Australia'):
        sum=sum + int(each.get('team1 Total'))
        count=count+1
    elif(each.get('team2')=='Australia'):
        sum=sum +int(each.get('team2 Total'))
        count=count+1

teamAvgScore=math.ceil(sum/count)

standardDeviation=team1AvgScore-teamAvgScore

print 'Standard Deviation for team Australia is ' +str(standardDeviation)        
                              
#print teamAvgScore
#print team1AvgScore