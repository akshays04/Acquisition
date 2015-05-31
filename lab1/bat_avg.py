from __future__ import division
import pymongo
import json

client = pymongo.MongoClient("localhost", 27017)

db = client.CricStats
#team1 = raw_input('Enter First Team')
#team2 = raw_input('Enter Second Team')
team1 = {}
team2 = {}
bat = {}
players1 = {}
players2 = {}

ourTeam = "India"
versus = "Australia"
currentYear = 2015

count = 0
for each in db.odi.find({"$or":[{"team1":ourTeam,"team2":versus},{"team1":versus,"team2":ourTeam}]}):
    #if(each.get('winner') == ourTeam):
    if(each.get('bat1')[0].get('team') == ourTeam):
        team1["team"] = ourTeam
        #print "******India Bat First******"
        for pl in each.get('bat1'):
            #print pl
            if(players1.has_key(pl.get('batsman'))):
                temp = players1[pl.get('batsman')]
                total = temp.get('tRuns')
                nom = temp.get('nom')
                nom += 1 
                total = total + int(pl.get('runs'))
                temp["tRuns"] = total
                temp["nom"] = nom
                players1[str(pl.get('batsman'))] = temp
               
            else:
                bat={} 
                bat["tRuns"] = int(pl.get('runs'))
                bat["nom"] = 1
                players1[str(pl.get('batsman'))] = bat
        team2["team"] = versus
        #print "******Aus Bat Second******"
        for pl in each.get('bat2'):
            #print pl
            if(players2.has_key(pl.get('batsman'))):
                temp = players2[pl.get('batsman')]
                total = temp.get('tRuns')
                nom = temp.get('nom')
                nom += 1 
                total = total + int(pl.get('runs'))
                temp["tRuns"] = total
                temp["nom"] = nom
                players2[str(pl.get('batsman'))] = temp
               
            else:
                bat={} 
                bat["tRuns"] = int(pl.get('runs'))
                bat["nom"] = 1
                players2[str(pl.get('batsman'))] = bat    
    else:
        team1["team"] = ourTeam
        #print "******India Bat Second******"
        for pl in each.get('bat2'):
            #print pl
            if(players1.has_key(pl.get('batsman'))):
                temp = players1[pl.get('batsman')]
                total = temp.get('tRuns')
                nom = temp.get('nom')
                nom += 1 
                total = total + int(pl.get('runs'))
                temp["tRuns"] = total
                temp["nom"] = nom
                players1[str(pl.get('batsman'))] = temp
               
            else:
                bat={} 
                bat["tRuns"] = int(pl.get('runs'))
                bat["nom"] = 1
                players1[str(pl.get('batsman'))] = bat
                
        team2["team"] = versus
        #print "******Aus Bat First******"
        for pl in each.get('bat1'):
            #print pl
            if(players2.has_key(pl.get('batsman'))):
                temp = players2[pl.get('batsman')]
                total = temp.get('tRuns')
                nom = temp.get('nom')
                nom += 1 
                total = total + int(pl.get('runs'))
                temp["tRuns"] = total
                temp["nom"] = nom
                players2[str(pl.get('batsman'))] = temp
               
            else:
                bat={} 
                bat["tRuns"] = int(pl.get('runs'))
                bat["nom"] = 1
                players2[str(pl.get('batsman'))] = bat     
    #print "*******************************************"
    
#print each    
for p in players1:
    temp = players1[p]
    avg = 0.0;
    avg = temp.get('tRuns') / temp.get('nom') 
    #print avg
    temp["avg"] = round(avg,2)
    players1[p] = temp

for p in players2:
    temp = players2[p]
    avg = 0.0;
    avg = temp.get('tRuns') / temp.get('nom') 
    #print avg
    temp["avg"] = round(avg,2)
    players2[p] = temp   
     
team1["players"] = players1
team2["players"] = players2

'''Avg print'''
#print team1
#print team2

ourTeamBatsman = []
if(team1["team"]==ourTeam):
    for each in team1["players"]:
        temp = {}
        #print team1["players"][each]
        temp = team1["players"][each]
        temp["batsman"] = each
        ourTeamBatsman.append(temp)
else:
    for each in team2["players"]:
        temp = {}
        #print team2["players"][each]
        temp = team2["players"][each]
        temp["batsman"] = each
        ourTeamBatsman.append(temp)

for i in range(0,len(ourTeamBatsman)):
    for j in range(0,len(ourTeamBatsman)-1):
        if ourTeamBatsman[j]["avg"] < ourTeamBatsman[j+1]["avg"]:
            temp = ourTeamBatsman[j]
            ourTeamBatsman[j] = ourTeamBatsman[j+1]
            ourTeamBatsman[j+1] = temp
           
print ourTeamBatsman


'''win % calc '''
teamBat1 = {}
teamBat2 = {}
bat = {}
latestPlayersWin = []
latestRecords = []
allRecords = []

for each in db.odi.find({"$or":[{"team1":ourTeam},{"team2":ourTeam}]}):
    arr = each.get("date").split(",")
    year = int(arr[1])
    if year == currentYear:
        latestRecords.append(each)
        
for each in db.odi.find({"$or":[{"team1":ourTeam},{"team2":ourTeam}]}):
    allRecords.append(each)

for each in db.odi.find({"$or":[{"team1":ourTeam,"team2":versus},{"team1":versus,"team2":ourTeam}]}):
     if(each.get('winner') == ourTeam):
        if(each.get('bat1')[0].get('team') == ourTeam):
            teamBat1["team"] = ourTeam
            #print "******India Bat First******"
            for pl in each.get('bat1'):
                #print pl
                bat["team"] = teamBat1["team"]
                bat["name"] = str(pl.get('batsman'))
                bat["runs"] = pl.get('runs')
                #bat["count"] = 0
                latestPlayersWin.append(bat)
                #print bat.team,bat.name 
#             teamBat2["team"] = versus
#             print "******AUS Bat Second******"
#             for pl in each.get('bat2'):
#                 print pl   
        else:
            teamBat1["team"] = ourTeam
            #print "******India Bat Second******"
            for pl in each.get('bat2'):
                #print pl
                bat={}
                bat["team"] = teamBat1["team"]
                bat["name"] = str(pl.get('batsman'))
                bat["runs"] = pl.get('runs')
                #bat["count"] = 0
                latestPlayersWin.append(bat)
latestPlayersLose = []      
for each in db.odi.find({"$or":[{"team1":ourTeam,"team2":versus},{"team1":versus,"team2":ourTeam}]}):
     if(each.get('winner') != ourTeam):
        if(each.get('bat1')[0].get('team') == ourTeam):
            teamBat1["team"] = ourTeam
            #print "******India Bat First******"
            for pl in each.get('bat1'):
                #print pl
                bat = {}
                bat["team"] = teamBat1["team"]
                bat["name"] = str(pl.get('batsman'))
                bat["runs"] = pl.get('runs')
                #bat["count"] = 0
                latestPlayersLose.append(bat)
                #print bat.team,bat.name 
#             teamBat2["team"] = versus
#             print "******AUS Bat Second******"
#             for pl in each.get('bat2'):
#                 print pl   
        else:
            teamBat1["team"] = ourTeam
            #print "******India Bat Second******"
            for pl in each.get('bat2'):
                #print pl
                bat={}
                bat["team"] = teamBat1["team"]
                bat["name"] = str(pl.get('batsman'))
                bat["runs"] = pl.get('runs')
                #bat["count"] = 0
                latestPlayersLose.append(bat)

#print latestPlayersWin
#print latestPlayersLose

topPlayerArr = []

for i in range(0,5):
    testPlayer = ourTeamBatsman[i]
    topPlayer = {}
    topPlayer["name"] = testPlayer["batsman"]
    topPlayer["avg"] = testPlayer["avg"]
    count50win = 0
    count75win = 0
    count100win = 0
    count50lose = 0
    count75lose = 0
    count100lose = 0
    for each in latestPlayersWin :
        if each.get("name")==topPlayer["name"]: 
            if(int(each["runs"])>50 and int(each["runs"])<75):
                count50win=count50win + 1
            if(int(each["runs"])>75 and int(each["runs"])<100):
                count75win= count75win + 1
            if(int(each["runs"])>100):
                count100win = count100win + 1
    for each in latestPlayersLose :
        if each.get("name")==topPlayer["name"]: 
            if(int(each["runs"])>50 and int(each["runs"])<75):
                count50lose=count50lose + 1
            if(int(each["runs"])>75 and int(each["runs"])<100):
                count75lose= count75lose + 1
            if(int(each["runs"])>100):
                count100lose = count100lose + 1
    if count50win+count50win !=0 : 
        win50 = float(count50win)/(float(count50win)+float(count50lose))
    else:
        win50 = 0.0
    if count75win+count75win !=0 : 
        win75 = float(count75win)/(float(count75win)+float(count75lose))
    else:
        win75 = 0.0
    if count100win+count100win !=0 : 
        win100 = float(count100win)/(float(count100win)+float(count100lose))
    else:
        win100 = 0.0
    win50 = win50 * 100.0
    win75 = win75 * 100
    win100 = win100 * 100
    combinedWin = win50+win75+win100
    topPlayer["combinedWin"] = round((combinedWin/300.0)*100.0, 2)
    topPlayer["count50win"] = count50win
    topPlayer["count75win"] = count75win
    topPlayer["count100win"] = count100win
    topPlayer["count50lose"] = count50lose
    topPlayer["count75lose"] = count75lose
    topPlayer["count100lose"] = count100lose
    topPlayer["win50"] = round(win50,2)
    topPlayer["win75"] = round(win75,2)
    topPlayer["win100"] = round(win100,2)
    scores=[]
    for each in latestRecords:
        if(each.get('bat1')[0].get('team') == ourTeam):
            for player in each.get('bat1'):
                if str(player.get('batsman'))==topPlayer["name"]:
                    temp = {}
                    temp["opponent"] = str(each.get("bat2")[0].get("team"))
                    temp["runs"] = int(player.get("runs"))
                    temp["balls"] = int(player.get("balls"))
                    #d = datetime.datetime.strptime(str(each.get("date")), '%d-%b-%y')
                    temp["date"] = str(each.get("date"))
                    temp["winner"] = str(each.get("winner"))
                    if(temp["winner"]==ourTeam):
                        temp["win"] = str(True)
                    else:
                        temp["win"] = str(False)
                    #print temp
                    scores.append(temp)                
        else:
            for player in each.get('bat2'):
                if str(player.get('batsman'))==topPlayer["name"]:
                    temp = {}
                    temp["opponent"] = str(each.get("bat1")[0].get("team"))
                    temp["runs"] = int(player.get("runs"))
                    temp["balls"] = int(player.get("balls"))
                    #d = datetime.datetime.strptime(str(each.get("date")), '%d-%b-%y')
                    temp["date"] = str(each.get("date"))
                    temp["winner"] = str(each.get("winner"))
                    if(temp["winner"]==ourTeam):
                        temp["win"] = str(True)
                    else:
                        temp["win"] = str(False)
                    scores.append(temp)
    topPlayer["latestRecords"] = scores
    scores=[]
    for each in allRecords:
        if(each.get('bat1')[0].get('team') == ourTeam):
            for player in each.get('bat1'):
                if str(player.get('batsman'))==topPlayer["name"]:
                    temp = {}
                    temp["opponent"] = str(each.get("bat2")[0].get("team"))
                    temp["runs"] = int(player.get("runs"))
                    #temp["balls"] = int(player.get("balls"))
                    #d = datetime.datetime.strptime(str(each.get("date")), '%d-%b-%y')
                    temp["date"] = str(each.get("date"))
                    temp["winner"] = str(each.get("winner"))
                    if(temp["winner"]==ourTeam):
                        temp["win"] = str(True)
                    else:
                        temp["win"] = str(False)
                    #print temp
                    scores.append(temp)                
        else:
            for player in each.get('bat2'):
                if str(player.get('batsman'))==topPlayer["name"]:
                    temp = {}
                    temp["opponent"] = str(each.get("bat1")[0].get("team"))
                    temp["runs"] = int(player.get("runs"))
                    temp["balls"] = int(player.get("balls"))
                    #d = datetime.datetime.strptime(str(each.get("date")), '%d-%b-%y')
                    temp["date"] = str(each.get("date"))
                    temp["winner"] = str(each.get("winner"))
                    if(temp["winner"]==ourTeam):
                        temp["win"] = str(True)
                    else:
                        temp["win"] = str(False)
                    scores.append(temp)
    topPlayer["allRecords"] = scores
    topPlayerArr.append(topPlayer)
    
newTopPlayerArr = []
for each in topPlayerArr:
    if len(each["latestRecords"]) != 0:
        newTopPlayerArr.append(each)
        
print len(newTopPlayerArr)

for i in range(0,len(newTopPlayerArr)):
    for j in range(0,len(newTopPlayerArr)-1):
        if newTopPlayerArr[j]["combinedWin"] < newTopPlayerArr[j+1]["combinedWin"]:
            temp = newTopPlayerArr[j]
            newTopPlayerArr[j] = newTopPlayerArr[j+1]
            newTopPlayerArr[j+1] = temp
    
print newTopPlayerArr

with open('batting.json', 'w') as outfile:
    json.dump(newTopPlayerArr, outfile)
    

if newTopPlayerArr[0]["win100"]>newTopPlayerArr[0]["win75"]:
    print "if "+newTopPlayerArr[0]["name"]+" scores more than 100 runs, "+ourTeam+" has "+str(newTopPlayerArr[0]["combinedWin"])+" % chance to win"
elif newTopPlayerArr[0]["win75"]>newTopPlayerArr[0]["win50"]:
    print "if "+newTopPlayerArr[0]["name"]+" scores more than 75 runs, "+ourTeam+" has "+str(newTopPlayerArr[0]["combinedWin"])+" % chance to win"
elif newTopPlayerArr[0]["win50"]>0.0:
    print "if "+newTopPlayerArr[0]["name"]+" scores more than 50 runs, "+ourTeam+" has "+str(newTopPlayerArr[0]["combinedWin"])+" % chance to win"
    
    
    
            
    