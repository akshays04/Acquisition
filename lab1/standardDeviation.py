import pymongo
import math

client = pymongo.MongoClient("localhost", 27017)
db = client.CricStats
count = 0
sum=0

ourTeam = "Australia"
location = "Sydney"
winScores = []
loseScores = []
for each in db.odi.find({"$or":[{ "team1":ourTeam, 'location': { '$in': [location ] } }, { "team2":ourTeam, 'location': { '$in': [location ] } }]}):
    if(each.get('winner') == ourTeam):
        if(each.get('bat1')[0].get('team') == ourTeam):
            score = {}
            score["batOrder"] = 1
            score["score"] = int((each.get('team1 Total')))
            score["date"] = str((each.get('date')))
            score["opponent"] = str(each.get('bat2')[0].get('team'))
            winScores.append(score)
        else:
            score = {}
            score["batOrder"] = 2
            score["score"] = int((each.get('team1 Total')))
            score["date"] = str((each.get('date')))
            score["opponent"] = str(each.get('bat1')[0].get('team'))
            winScores.append(score)
    else:
        if(each.get('bat1')[0].get('team') == ourTeam):
            score = {}
            score["batOrder"] = 1
            score["score"] = int((each.get('team1 Total')))
            score["opponent"] = str(each.get('bat2')[0].get('team'))
            score["date"] = str((each.get('date')))
            loseScores.append(score)
        else:
            score = {}
            score["batOrder"] = 2
            score["score"] = int((each.get('team1 Total')))
            score["opponent"] = str(each.get('bat1')[0].get('team'))
            score["date"] = str((each.get('date')))
            loseScores.append(score)
#print winScores
#print loseScores
batFirstWins = []
batSecondWins = []
batFirstLoss = []
batSecondLoss = []
for each in winScores:
    if each["batOrder"] == 1:
        batFirstWins.append(each)
    else:
        batSecondWins.append(each)

for each in loseScores:
    if each["batOrder"] == 1:
        batFirstLoss.append(each)
    else:
        batSecondLoss.append(each)
        
print batFirstWins
print batFirstLoss
print batSecondWins
print batSecondLoss

if (len(batFirstWins) + len(batFirstLoss)) > 0:
    batFirstPercent = float(len(batFirstWins))/float((len(batFirstWins) + len(batFirstLoss)))
    batFirstPercent = batFirstPercent * 100
    batFirstPercent = round(batFirstPercent, 2)
else:
    batFirstPercent = 0.0
    
if (len(batSecondWins) + len(batSecondLoss)) > 0:
    batSecondPercent = float(len(batSecondWins))/float((len(batSecondWins) + len(batSecondLoss)))
    batSecondPercent = batSecondPercent * 100
    batSecondPercent = round(batSecondPercent, 2)
else:
    batSecondPercent = 0.0
    
print "Bat First : "+str(batFirstPercent)
print "Bat Second : "+str(batSecondPercent)

optimumScoreBat1 = 0
optimumBat1Percent = 0.0
optimumScoreBat2 = 0
optimumBat2Percent = 0.0
flag = True
flagFound = False

scoreRecordsB1 = []
for each in (batFirstWins+batFirstLoss):
    score = {}
    score["score"] = each["score"]
    score["winCountb1"] = 0
    score["loseCountb1"] = 0
    scoreRecordsB1.append(score)
    
scoreRecordsB2 = []
for each in (batSecondWins+batSecondLoss):
    score = {}
    score["score"] = each["score"]
    score["winCountb2"] = 0
    score["loseCountb2"] = 0
    scoreRecordsB2.append(score)

for each in batFirstWins:
    for temp in scoreRecordsB1:
        if each["score"]<=temp["score"]:
            temp["winCountb1"] = temp["winCountb1"] + 1
            
for each in batSecondWins:
    for temp in scoreRecordsB2:
        if each["score"]>=temp["score"]:
            temp["winCountb2"] = temp["winCountb2"] + 1
            
for each in batFirstLoss:
    for temp in scoreRecordsB1:
        if each["score"]>=temp["score"]:
            temp["loseCountb1"] = temp["loseCountb1"] + 1
            
for each in batSecondLoss:
    for temp in scoreRecordsB2:
        if each["score"]<=temp["score"]:
            temp["loseCountb2"] = temp["loseCountb2"] + 1

for each in scoreRecordsB1:
    each["winPercent"] = round(float(each["winCountb1"]) / float(each["winCountb1"] + each["loseCountb1"]), 2) * 100
    
for each in scoreRecordsB2:
    each["winPercent"] = round(float(each["winCountb2"]) / float(each["winCountb2"] + each["loseCountb2"]), 2) * 100
    
for i in range(0,len(scoreRecordsB1)):
    for j in range(0,len(scoreRecordsB1)-1):
        if scoreRecordsB1[j]["winPercent"] == scoreRecordsB1[j+1]["winPercent"]:
            if scoreRecordsB1[j]["score"] > scoreRecordsB1[j+1]["score"]:
                temp = scoreRecordsB1[j]
                scoreRecordsB1[j] = scoreRecordsB1[j+1]
                scoreRecordsB1[j+1] = temp
        elif scoreRecordsB1[j]["winPercent"] < scoreRecordsB1[j+1]["winPercent"]:
            temp = scoreRecordsB1[j]
            scoreRecordsB1[j] = scoreRecordsB1[j+1]
            scoreRecordsB1[j+1] = temp
            
for i in range(0,len(scoreRecordsB2)):
    for j in range(0,len(scoreRecordsB2)-1):
        if scoreRecordsB2[j]["winPercent"] == scoreRecordsB2[j+1]["winPercent"]:
            if scoreRecordsB2[j]["score"] < scoreRecordsB2[j+1]["score"]:
                temp = scoreRecordsB2[j]
                scoreRecordsB2[j] = scoreRecordsB2[j+1]
                scoreRecordsB2[j+1] = temp
        elif scoreRecordsB2[j]["winPercent"] < scoreRecordsB2[j+1]["winPercent"]:
            temp = scoreRecordsB2[j]
            scoreRecordsB2[j] = scoreRecordsB2[j+1]
            scoreRecordsB2[j+1] = temp
    
print scoreRecordsB1
print scoreRecordsB2
       
'''
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
'''