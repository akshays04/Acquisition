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
with open('input.json') as data_file:    
    input = json.load(data_file)
    ourTeam = input["ourTeam"]
    versus = input["versus"]
    location = input["location"]
#ourTeam = "Australia"
#versus = "India"
currentYear = 2015

count = 0
for each in db.odi.find({"$or":[{"team1":ourTeam,"team2":versus},{"team1":versus,"team2":ourTeam}]}):
    #if(each.get('winner') == ourTeam):
    if(each.get('bowl1')[0].get('team') == ourTeam):
        team1["team"] = ourTeam
        #print each.get('bowl1')
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
        if(each.get('bowl2')[0].get('team') == ourTeam):
            #print each.get('bowl2')
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
    
print players1
print players2
    
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
finalArr = []
for i in range(0,10):
    bowl = teamArr[i]
    if bowl["name"] in bowlerRecords:
        if ((bowlerRecords[bowl["name"]]['winCount3wkt'] + bowlerRecords[bowl["name"]]['loseCount3wkt']) == 0):
            win3wkt = 0.0
        else:
            win3wkt = bowlerRecords[bowl["name"]]['winCount3wkt']  /    (bowlerRecords[bowl["name"]]['winCount3wkt'] + bowlerRecords[bowl["name"]]['loseCount3wkt'])
            win3wkt = win3wkt * 100
            win3wkt = round(win3wkt,2)
        if (bowlerRecords[bowl["name"]]['winCount3Eco'] + bowlerRecords[bowl["name"]]['loseCount3Eco']) == 0 : 
            win3Eco = 0.0
        else:        
            win3Eco = bowlerRecords[bowl["name"]]['winCount3Eco']  /    (bowlerRecords[bowl["name"]]['winCount3Eco'] + bowlerRecords[bowl["name"]]['loseCount3Eco'])
            win3Eco = win3Eco * 100
            win3Eco = round(win3Eco,2)
        if  (bowlerRecords[bowl["name"]]['winCount5wkt'] + bowlerRecords[bowl["name"]]['loseCount5wkt']) == 0:
            win5wkt = 0.0
        else:
            win5wkt = bowlerRecords[bowl["name"]]['winCount5wkt']  /    (bowlerRecords[bowl["name"]]['winCount5wkt'] + bowlerRecords[bowl["name"]]['loseCount5wkt'])
            win5wkt = win5wkt * 100
            win5wkt = round(win5wkt,2)
        combinedWin = (win3wkt + win3Eco + win5wkt)/300
        combinedWin = round(combinedWin * 100, 2)
        bowl["win3wkt"] = win3wkt
        bowl["win3Eco"] = win3Eco
        bowl["win5wkt"] = win5wkt
        bowl["combinedWin"] = combinedWin
        finalArr.append(bowl)
    

for i in range(0,len(finalArr)):
    for j in range(0,len(finalArr)-1):
        if finalArr[j]["combinedWin"] < finalArr[j+1]["combinedWin"]:
            temp = finalArr[j]
            finalArr[j] = finalArr[j+1]
            finalArr[j+1] = temp
print finalArr
bowler = finalArr[0]

playerLatestRecords = []
for each in db.odi.find({"$or":[{"team1":ourTeam},{"team2":ourTeam}]}):
        if(each.get('bowl1')[0].get('team') == ourTeam):
            for pl in each.get('bowl1'):
                if pl.get("bowler") == bowler["name"]:
                    bowl = {}
                    datesplit=str(each.get("date")).split(',',2)
                    year=datesplit[1].strip()[2:]
                    dmonthsplit=datesplit[0].split(' ',2)
                    month=dmonthsplit[0]
                    day=dmonthsplit[1]
                    if (each["winner"] == ourTeam):
                        bowl["win"] = "True"
                    else:
                        bowl["win"] = "False"
                    bowl["date"] = day+'-'+month+'-'+year
                    bowl["wkt"] = int(pl.get('wickets'))
                    bowl["eco"] = float(pl.get("economy"))
                    playerLatestRecords.append(bowl)
        elif (each.get('bowl2')[0].get('team') == ourTeam):
            for pl in each.get('bowl2'):
                if pl.get("bowler") == bowler["name"]:
                    bowl = {}
                    datesplit=str(each.get("date")).split(',',2)
                    year=datesplit[1].strip()[2:]
                    dmonthsplit=datesplit[0].split(' ',2)
                    month=dmonthsplit[0]
                    day=dmonthsplit[1]
                    if (each["winner"] == ourTeam):
                        bowl["win"] = "True"
                    else:
                        bowl["win"] = "False"
                    bowl["date"] = day+'-'+month+'-'+year
                    bowl["wkt"] = int(pl.get('wickets'))
                    bowl["eco"] = float(pl.get("economy"))
                    playerLatestRecords.append(bowl)

finalArr[0]["allRecords"] = playerLatestRecords
with open('bowling.json', 'w') as outfile:
    json.dump(finalArr, outfile)

bowlingStr = ""
bowlingPercent = 0.0   
if finalArr[0]["win5wkt"]>=finalArr[0]["win3Eco"]:
    bowlingStr = "if "+finalArr[0]["name"]+" takes 5 wickets in an innings, "+ourTeam+" has "+str(finalArr[0]["combinedWin"])+" % chance to win"
    bowlingPercent = (finalArr[0]["combinedWin"] / 100.0) * 20.0
    print bowlingStr
elif finalArr[0]["win3Eco"]>=finalArr[0]["win3wkt"]:
    bowlingStr = "if "+finalArr[0]["name"]+" takes 3 wickets at an economy of 4.5 runs per over, "+ourTeam+" has "+str(finalArr[0]["combinedWin"])+" % chance to win"
    bowlingPercent = (finalArr[0]["combinedWin"] / 100.0) * 20.0
    print bowlingStr
elif finalArr[0]["win3wkt"]>0.0:
    bowlingStr = "if "+finalArr[0]["name"]+" takes 3 wickets, "+ourTeam+" has "+str(finalArr[0]["combinedWin"])+" % chance to win"
    bowlingPercent = (finalArr[0]["combinedWin"] / 100.0) * 20.0
    print bowlingStr
    
with open('data.json') as data_file:    
    data = json.load(data_file)
    data["bowlingStr"] = bowlingStr
    data["bowlingPercent"] = round(bowlingPercent, 2)
    
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
    
    