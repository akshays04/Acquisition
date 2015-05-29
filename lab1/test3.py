import pymongo

client = pymongo.MongoClient("localhost", 27017)

db = client.CricStats
count = 0
latestRecords = []
for each in db.odi.find({"$or":[{"teamBat1":"India"},{"teamBat2":"India"}]}):
    arr = each.get("date").split(",")
    year = int(arr[1])
    if year == 2015:
        latestRecords.append(each)
    count = count+1
#print count
#print len(latestRecords)
teamBat1 = {}
teamBat2 = {}
bat = {}
latestBatsmanRecords = []

for each in latestRecords:
    if(each.get('bat1')[0].get('team') == "India"):
            teamBat1["team"] = "India"
            #print "******India Bat First******"
            for pl in each.get('bat1'):
                #print pl
                bat = {}
                bat["team"] = teamBat1["team"]
                bat["name"] = str(pl.get('batsman'))
                bat["runs"] = pl.get('runs')
                #bat["count"] = 0
                latestBatsmanRecords.append(bat)
                #print bat.team,bat.name 
#             teamBat2["team"] = "Australia"
#             print "******AUS Bat Second******"
#             for pl in each.get('bat2'):
#                 print pl   
    else:
        teamBat1["team"] = "India"
        #print "******India Bat Second******"
        for pl in each.get('bat2'):
            #print pl
            bat={}
            bat["team"] = teamBat1["team"]
            bat["name"] = str(pl.get('batsman'))
            bat["runs"] = pl.get('runs')
            #bat["count"] = 0
            latestBatsmanRecords.append(bat)



topPlayer = {}
for each in latestBatsmanRecords:
    if(int(each["runs"])>80):
        if topPlayer.has_key(each.get("name")):
            temp = topPlayer[each.get("name")]
            topPlayer[each.get("name")] = temp + 1
        else:
            topPlayer[each.get("name")] = 1

print topPlayer

'''Start of win % calculation'''
teamBat1 = {}
teamBat2 = {}
bat = {}
latestPlayersWin = []

for each in db.odi.find({"$or":[{"teamBat1":"India","teamBat2":"Australia"},{"teamBat1":"Australia","teamBat2":"India"}]}):
     if(each.get('winner') == "India"):
        if(each.get('bat1')[0].get('team') == "India"):
            teamBat1["team"] = "India"
            #print "******India Bat First******"
            for pl in each.get('bat1'):
                #print pl
                bat["team"] = teamBat1["team"]
                bat["name"] = str(pl.get('batsman'))
                bat["runs"] = pl.get('runs')
                #bat["count"] = 0
                latestPlayersWin.append(bat)
                #print bat.team,bat.name 
#             teamBat2["team"] = "Australia"
#             print "******AUS Bat Second******"
#             for pl in each.get('bat2'):
#                 print pl   
        else:
            teamBat1["team"] = "India"
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
for each in db.odi.find({"$or":[{"teamBat1":"India","teamBat2":"Australia"},{"teamBat1":"Australia","teamBat2":"India"}]}):
     if(each.get('winner') != "India"):
        if(each.get('bat1')[0].get('team') == "India"):
            teamBat1["team"] = "India"
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
#             teamBat2["team"] = "Australia"
#             print "******AUS Bat Second******"
#             for pl in each.get('bat2'):
#                 print pl   
        else:
            teamBat1["team"] = "India"
            #print "******India Bat Second******"
            for pl in each.get('bat2'):
                #print pl
                bat={}
                bat["team"] = teamBat1["team"]
                bat["name"] = str(pl.get('batsman'))
                bat["runs"] = pl.get('runs')
                #bat["count"] = 0
                latestPlayersLose.append(bat)
topPlayerWin = {}        
for each in latestPlayersWin : 
    if(int(each["runs"])>50):
        if topPlayerWin.has_key(each.get("name")):
            temp = topPlayerWin[each.get("name")]
            topPlayerWin[each.get("name")] = temp + 1
        else:
            topPlayerWin[each.get("name")] = 1
        #print each
        
#print "************************"

topPlayerLose = {} 
for each in latestPlayersLose : 
    if(int(each["runs"])>50):
        if topPlayerLose.has_key(each.get("name")) :
            temp = topPlayerLose[each.get("name")]
            topPlayerLose[each.get("name")] = temp + 1
        else:
            topPlayerLose[each.get("name")] = 1
        #print each
        

winPercent = {}
for each in topPlayerWin.keys():
    if(topPlayerLose.has_key(each)):
        sum = topPlayerLose[each]+topPlayerWin[each]
        floatCalc = float(topPlayerWin[each])/float(sum)
        winPercent[each] = floatCalc*100
    else:
        winPercent[each] = 100
        
#print topPlayerWin
#print topPlayerLose
print "winpercent "+str(winPercent)