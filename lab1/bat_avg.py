from __future__ import division
import pymongo


client = pymongo.MongoClient("localhost", 27017)

db = client.CricStats
#team1 = raw_input('Enter First Team')
#team2 = raw_input('Enter Second Team')
team1 = {}
team2 = {}
bat = {}
players1 = {}
players2 = {}

count = 0
for each in db.odi.find({"$or":[{"team1":"India","team2":"Australia"},{"team1":"Australia","team2":"India"}]}):
    #if(each.get('winner') == "India"):
    if(each.get('bat1')[0].get('team') == "India"):
        team1["team"] = "India"
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
        team2["team"] = "Australia"
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
        team1["team"] = "India"
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
                
        team2["team"] = "Australia"
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
    
print each    
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

print team1
print team2

    
    