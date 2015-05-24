import pymongo

client = pymongo.MongoClient("localhost", 27017)

db = client.CricStats
count = 0
latestRecords = []
for each in db.odi.find({"$or":[{"team1":"India"},{"team2":"India"}]}):
    arr = each.get("date").split(",")
    year = int(arr[1])
    if year == 2015:
        latestRecords.append(each)
    count = count+1
print count
print len(latestRecords)

team1 = {}
team2 = {}
bat = {}
latestPlayersWin = []

for each in db.odi.find({"$or":[{"team1":"India","team2":"Australia"},{"team1":"Australia","team2":"India"}]}):
     if(each.get('winner') == "India"):
        if(each.get('bat1')[0].get('team') == "India"):
            team1["team"] = "India"
            #print "******India Bat First******"
            for pl in each.get('bat1'):
                #print pl
                bat["team"] = team1["team"]
                bat["name"] = str(pl.get('batsman'))
                bat["runs"] = pl.get('runs')
                #bat["count"] = 0
                latestPlayersWin.append(bat)
                #print bat.team,bat.name 
#             team2["team"] = "Australia"
#             print "******AUS Bat Second******"
#             for pl in each.get('bat2'):
#                 print pl   
        else:
            team1["team"] = "India"
            #print "******India Bat Second******"
            for pl in each.get('bat2'):
                #print pl
                bat={}
                bat["team"] = team1["team"]
                bat["name"] = str(pl.get('batsman'))
                bat["runs"] = pl.get('runs')
                #bat["count"] = 0
                latestPlayersWin.append(bat)
latestPlayersLose = []      
for each in db.odi.find({"$or":[{"team1":"India","team2":"Australia"},{"team1":"Australia","team2":"India"}]}):
     if(each.get('winner') != "India"):
        if(each.get('bat1')[0].get('team') == "India"):
            team1["team"] = "India"
            #print "******India Bat First******"
            for pl in each.get('bat1'):
                #print pl
                bat = {}
                bat["team"] = team1["team"]
                bat["name"] = str(pl.get('batsman'))
                bat["runs"] = pl.get('runs')
                #bat["count"] = 0
                latestPlayersLose.append(bat)
                #print bat.team,bat.name 
#             team2["team"] = "Australia"
#             print "******AUS Bat Second******"
#             for pl in each.get('bat2'):
#                 print pl   
        else:
            team1["team"] = "India"
            #print "******India Bat Second******"
            for pl in each.get('bat2'):
                #print pl
                bat={}
                bat["team"] = team1["team"]
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
        print each
        
print "************************"

topPlayerLose = {} 
for each in latestPlayersLose : 
    if(int(each["runs"])>50):
        if topPlayerLose.has_key(each.get("name")) :
            temp = topPlayerLose[each.get("name")]
            topPlayerLose[each.get("name")] = temp + 1
        else:
            topPlayerLose[each.get("name")] = 1
        print each
print topPlayerWin
print topPlayerLose