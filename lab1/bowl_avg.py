from __future__ import division
import pymongo
import json


client = pymongo.MongoClient("localhost", 27017)

db = client.CricStats
#team1 = raw_input('Enter First Team')
#team2 = raw_input('Enter Second Team')
team1 = {}
team2 = {}
bowl = {}
players1 = {}
players2 = {}
ourTeam = "India"
versus = "Sri Lanka"
currentYear = 2015

count = 0
for each in db.odi.find({"$or":[{"team1":ourTeam,"team2":versus},{"team1":versus,"team2":ourTeam}]}):
    #if(each.get('winner') == ourTeam):
    if(each.get('bowl1')[0].get('team') == ourTeam):
        team1["team"] = ourTeam
        #print "******India bowl First******"
        for pl in each.get('bowl1'):
            #print pl
            if(players1.has_key(pl.get('bowler'))):
                temp = players1[pl.get('bowler')]
                total = temp.get('wkt')
                eco = temp.get('eco')
                nom = temp.get('nom')
                nom += 1 
                eco = eco + float(pl.get('economy')) 
                total = total + int(int(pl.get('wickets')))
                temp["wkt"] = total
                temp["nom"] = nom
                temp["eco"] = eco
                players1[str(pl.get('bowler'))] = temp
               
            else:
                bowl={} 
                bowl["wkt"] = int(int(pl.get('wickets')))
                bowl["eco"] = float(pl.get('economy'))
                bowl["nom"] = 1
                players1[str(pl.get('bowler'))] = bowl
        team2["team"] = versus
        #print "******Aus bowl Second******"
        for pl in each.get('bowl2'):
            #print pl
            if(players2.has_key(pl.get('bowler'))):
                temp = players2[pl.get('bowler')]
                total = temp.get('wkt')
                eco = temp.get('eco')
                nom = temp.get('nom')
                nom += 1 
                eco = eco + float(pl.get('economy')) 
                total = total + int(int(pl.get('wickets')))
                temp["wkt"] = total
                temp["nom"] = nom
                temp["eco"] = eco
                players2[str(pl.get('bowler'))] = temp
               
            else:
                bowl={} 
                bowl["wkt"] = int(int(pl.get('wickets')))
                bowl["nom"] = 1
                bowl["eco"] = float(pl.get('economy'))
                players2[str(pl.get('bowler'))] = bowl    
    else:
        team1["team"] = ourTeam
        #print "******India bowl Second******"
        for pl in each.get('bowl2'):
            #print pl
            if(players1.has_key(pl.get('bowler'))):
                temp = players1[pl.get('bowler')]
                total = temp.get('wkt')
                eco = temp.get('eco')
                nom = temp.get('nom')
                nom += 1 
                eco = eco + float(pl.get('economy')) 
                total = total + int(int(pl.get('wickets')))
                temp["wkt"] = total
                temp["nom"] = nom
                temp["eco"] = eco
                players1[str(pl.get('bowler'))] = temp
               
            else:
                bowl={} 
                bowl["wkt"] = int(int(pl.get('wickets')))
                bowl["eco"] = float(pl.get('economy'))
                bowl["nom"] = 1
                players1[str(pl.get('bowler'))] = bowl
                
        team2["team"] = versus
        #print "******Aus bowl First******"
        for pl in each.get('bowl1'):
            #print pl
            if(players2.has_key(pl.get('bowler'))):
                temp = players2[pl.get('bowler')]
                total = temp.get('wkt')
                eco = temp.get('eco')
                nom = temp.get('nom')
                nom += 1 
                eco = eco + float(pl.get('economy')) 
                total = total + int(int(pl.get('wickets')))
                temp["wkt"] = total
                temp["nom"] = nom
                temp["eco"] = eco
                players2[str(pl.get('bowler'))] = temp
               
            else:
                bowl={} 
                bowl["wkt"] = int(int(pl.get('wickets')))
                bowl["nom"] = 1
                bowl["eco"] = float(pl.get('economy'))
                players2[str(pl.get('bowler'))] = bowl       
    #print "*******************************************"
    
#print each    
for p in players1:
    temp = players1[p]
    avg = 0.0;
    avg = temp.get('eco') / temp.get('nom') 
    #print avg
    temp["eco"] = round(avg,2)
    players1[p] = temp

for p in players2:
    temp = players2[p]
    avg = 0.0;
    avg = temp.get('eco') / temp.get('nom') 
    #print avg
    temp["eco"] = round(avg,2)
    players2[p] = temp   
     
team1["players"] = players1
team2["players"] = players2

for each in team1["players"]:
    avg = 0.0
    avg = team1["players"][each]["wkt"]/team1["players"][each]["nom"]
    team1["players"][each]["wktavg"] = round(avg,2)
    
for each in team2["players"]:
    avg = 0.0
    avg = team2["players"][each]["wkt"]/team2["players"][each]["nom"]
    team2["players"][each]["wktavg"] = round(avg,2)

print team1
teamArr = []
for each in team1["players"]:
    bowl = team1["players"][each]
    bowl["name"] = each
    teamArr.append(bowl)
#print team2

for each in teamArr:
    if each["nom"]<3:
        teamArr.remove(each)

for i in range(0,len(teamArr)):
    for j in range(0,len(teamArr)-1):
        if teamArr[j]["wktavg"] < teamArr[j+1]["wktavg"]:
            temp = teamArr[j]
            teamArr[j] = teamArr[j+1]
            teamArr[j+1] = temp
    
print teamArr

'''win % calculation'''
latestRecords = []

for each in db.odi.find({"$or":[{"team1":ourTeam},{"team2":ourTeam}]}):
    arr = each.get("date").split(",")
    year = int(arr[1])
    if year == currentYear:
        latestRecords.append(each)
        
teamBowl1 = {}
teamBowl2 = {}
latestPlayersWin = []

'''doubtful section '''
for each in latestRecords:
     if(each.get('winner') == ourTeam):
        if(each.get('bowl1')[0].get('team') == ourTeam):
            teamBowl1["team"] = ourTeam
            #print "******India Bat First******"
            for pl in each.get('bowl1'):
                #print pl
                bowl = {}
                bowl["team"] = teamBowl1["team"]
                bowl["name"] = str(pl.get('bowler'))
                bowl["wkt"] = int(pl.get('wickets'))
                bowl["eco"] = float(pl.get("economy"))
                #bat["count"] = 0
                latestPlayersWin.append(bowl)
                #print bat.team,bat.name 
#             teambowl2["team"] = versus
#             print "******AUS Bat Second******"
#             for pl in each.get('bowl2'):
#                 print pl   
        else:
            teamBowl2["team"] = ourTeam
            #print "******India Bat Second******"
            for pl in each.get('bowl2'):
                #print pl
                bowl = {}
                bowl["team"] = teamBowl2["team"]
                bowl["name"] = str(pl.get('bowler'))
                bowl["wkt"] = int(pl.get('wickets'))
                bowl["eco"] = float(pl.get("economy"))
                latestPlayersWin.append(bowl)
latestPlayersLose = []      
for each in db.odi.find({"$or":[{"team1":ourTeam,"team2":versus},{"team1":versus,"team2":ourTeam}]}):
     if(each.get('winner') != ourTeam):
        if(each.get('bowl1')[0].get('team') == ourTeam):
            teamBowl1["team"] = ourTeam
            #print "******India Bat First******"
            for pl in each.get('bowl1'):
                #print pl
                bowl = {}
                bowl["team"] = teamBowl1["team"]
                bowl["name"] = str(pl.get('bowler'))
                bowl["wkt"] = int(pl.get('wickets'))
                bowl["eco"] = float(pl.get("economy"))
                #bat["count"] = 0
                latestPlayersLose.append(bowl)
                #print bat.team,bat.name 
#             teambowl2["team"] = versus
#             print "******AUS Bat Second******"
#             for pl in each.get('bowl2'):
#                 print pl   
        else:
            teamBowl2["team"] = ourTeam
            #print "******India Bat Second******"
            for pl in each.get('bowl2'):
                #print pl
                bowl = {}
                bowl["team"] = teamBowl1["team"]
                bowl["name"] = str(pl.get('bowler'))
                bowl["wkt"] = int(pl.get('wickets'))
                bowl["eco"] = float(pl.get("economy"))
                latestPlayersLose.append(bowl)
                
print "-------------------------"
print latestPlayersWin
print latestPlayersLose

bowlerRecords = {}
for each in latestPlayersWin:
    bowl = {}
    if each["name"] in bowlerRecords:
        bowl = bowlerRecords[each["name"]]
        if each["wkt"] >=3 :
            bowl["winCount3wkt"] = bowl["winCount3wkt"] + 1
        if each["wkt"] >=3 and each["eco"] <= 4.5:
            bowl["winCount3Eco"] = bowl["winCount3Eco"] + 1
        if each["wkt"] >=5:
            bowl["winCount5wkt"] = bowl["winCount5wkt"] + 1
        bowlerRecords[each["name"]] = bowl
    else:
        bowl["winCount3wkt"] = 0
        bowl["winCount3Eco"] = 0
        bowl["winCount5wkt"] = 0
        bowl["loseCount3wkt"] = 0
        bowl["loseCount3Eco"] = 0
        bowl["loseCount5wkt"] = 0
        if each["wkt"] >=3 :
            bowl["winCount3wkt"] = bowl["winCount3wkt"] + 1
        if each["wkt"] >=3 and each["eco"] <= 4.5:
            bowl["winCount3Eco"] = bowl["winCount3Eco"] + 1
        if each["wkt"] >=5:
            bowl["winCount5wkt"] = bowl["winCount5wkt"] + 1
        bowlerRecords[each["name"]] = bowl

for each in latestPlayersLose:
    bowl = {}
    if each["name"] in bowlerRecords:
        bowl = bowlerRecords[each["name"]]
        if each["wkt"] >=3 :
            bowl["loseCount3wkt"] = bowl["loseCount3wkt"] + 1
        if each["wkt"] >=3 and each["eco"] <= 4.5:
            bowl["loseCount3Eco"] = bowl["loseCount3Eco"] + 1
        if each["wkt"] >=5:
            bowl["loseCount5wkt"] = bowl["loseCount5wkt"] + 1
        bowlerRecords[each["name"]] = bowl
    else:
        bowl["winCount3wkt"] = 0
        bowl["winCount3Eco"] = 0
        bowl["winCount5wkt"] = 0
        bowl["loseCount3wkt"] = 0
        bowl["loseCount3Eco"] = 0
        bowl["loseCount5wkt"] = 0
        if each["wkt"] >=3 :
            bowl["loseCount3wkt"] = bowl["loseCount3wkt"] + 1
        if each["wkt"] >=3 and each["eco"] <= 4.5:
            bowl["loseCount3Eco"] = bowl["loseCount3Eco"] + 1
        if each["wkt"] >=5:
            bowl["loseCount5wkt"] = bowl["loseCount5wkt"] + 1
        bowlerRecords[each["name"]] = bowl

print bowlerRecords


    
    