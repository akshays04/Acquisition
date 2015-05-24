from __future__ import division
import pymongo


client = pymongo.MongoClient("localhost", 27017)

db = client.CricStats
#team1 = raw_input('Enter First Team')
#team2 = raw_input('Enter Second Team')
team1 = {}
team2 = {}
bat = {}
players = {}
count = 0
for each in db.odi.find({"$or":[{"team1":"India","team2":"Australia"},{"team1":"Australia","team2":"India"}]}):
    if(each.get('winner') == "India"):
        if(each.get('bat1')[0].get('team') == "India"):
            team1["team"] = "India"
            print "******India Bat First******"
            for pl in each.get('bat1'):
                print pl
                if(players.has_key(pl.get('batsman'))):
                    temp = players[pl.get('batsman')]
                    total = temp.get('tRuns')
                    nom = temp.get('nom')
                    nom += 1 
                    total = total + int(pl.get('runs'))
                    temp["tRuns"] = total
                    temp["nom"] = nom
                    players[pl.get('batsman')] = temp
                   
                else:
                    bat={} 
                    bat["tRuns"] = int(pl.get('runs'))
                    bat["nom"] = 1
                    players[pl.get('batsman')] = bat
            team2["team"] = "Australia"
            print "******Aus Bat Second******"
            for pl in each.get('bat2'):
                print pl
                if(players.has_key(pl.get('batsman'))):
                    temp = players[pl.get('batsman')]
                    total = temp.get('tRuns')
                    nom = temp.get('nom')
                    nom += 1 
                    total = total + int(pl.get('runs'))
                    temp["tRuns"] = total
                    temp["nom"] = nom
                    players[pl.get('batsman')] = temp
                   
                else:
                    bat={} 
                    bat["tRuns"] = int(pl.get('runs'))
                    bat["nom"] = 1
                    players[pl.get('batsman')] = bat    
        else:
            team1["team"] = "India"
            print "******India Bat Second******"
            for pl in each.get('bat2'):
                print pl
                if(players.has_key(pl.get('batsman'))):
                    temp = players[pl.get('batsman')]
                    total = temp.get('tRuns')
                    nom = temp.get('nom')
                    nom += 1 
                    total = total + int(pl.get('runs'))
                    temp["tRuns"] = total
                    temp["nom"] = nom
                    players[pl.get('batsman')] = temp
                   
                else:
                    bat={} 
                    bat["tRuns"] = int(pl.get('runs'))
                    bat["nom"] = 1
                    players[pl.get('batsman')] = bat
                    
            team2["team"] = "Australia"
            print "******Aus Bat First******"
            for pl in each.get('bat1'):
                print pl
                if(players.has_key(pl.get('batsman'))):
                    temp = players[pl.get('batsman')]
                    total = temp.get('tRuns')
                    nom = temp.get('nom')
                    nom += 1 
                    total = total + int(pl.get('runs'))
                    temp["tRuns"] = total
                    temp["nom"] = nom
                    players[pl.get('batsman')] = temp
                   
                else:
                    bat={} 
                    bat["tRuns"] = int(pl.get('runs'))
                    bat["nom"] = 1
                    players[pl.get('batsman')] = bat     
    print "*******************************************"
    
print each    
for p in players:
    temp = players[p]
    avg = 0.0;
    avg = temp.get('tRuns') / temp.get('nom') 
    #print avg
    temp["avg"] = avg
    players[p] = temp

print players

    
    