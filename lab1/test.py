from __future__ import division
import pymongo


client = pymongo.MongoClient("localhost", 27017)

db = client.CricStats
#team1 = raw_input('Enter First Team')
#team2 = raw_input('Enter Second Team')
team1 = {}
team2 = {}
bat = {}
players = []
count = 0
for each in db.odi.find({"$or":[{"team1":"India","team2":"Australia"},{"team1":"Australia","team2":"India"}]}):
    if(each.get('winner') == "India"):
        if(each.get('bat1')[0].get('team') == "India"):
            team1["team"] = "India"
            print "******India Bat First******"
            for pl in each.get('bat1'):
                print pl
                bat["team"] = team1["team"]
                bat["name"] = pl.batsman
                print bat.team,bat.name 
#             team2["team"] = "Australia"
#             print "******AUS Bat Second******"
#             for pl in each.get('bat2'):
#                 print pl   
        else:
            team1["team"] = "India"
            print "******India Bat Second******"
            for pl in each.get('bat2'):
                print pl
                bat={}
                bat["team"] = team1["team"]
                bat["name"] = pl.get('batsman')
                bat["runs"] = pl.get('runs')
                players.append(bat)

                #print bat.get('team'),bat.get('name')
#                 if(db.odi.find({"bat1":"S Dhawan"})):
#                     print "yes"
#             team2["team"] = "Australia"
#             print "******Aus Bat First******"
#             for pl in each.get('bat1'):
#                 print pl
#             # print each.get('winner')
    print "*******************************************"
    
print each

for p in players:
    total = 0;
    count = 0;
    for q in players:
        if(p.get('name') == q.get('name')):
            #print q.get('name')
            total =int(total) + int(q.get('runs'))
            count += 1;
            p["nom"] = count
     
    #print p.get('name'),total,p.get('count')
    p["tRuns"] = total
    
for p in players:
    avg = 0.0;
    avg = p.get('tRuns') / p.get('nom') 
    #print avg
    p["avg"] = avg

for p in players:
    print p.get('name'),p.get('tRuns'),p.get('avg')
    
    