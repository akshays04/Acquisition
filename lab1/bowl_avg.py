from __future__ import division
import pymongo


client = pymongo.MongoClient("localhost", 27017)

db = client.CricStats
#team1 = raw_input('Enter First Team')
#team2 = raw_input('Enter Second Team')
team1 = {}
team2 = {}
bowl = {}
players1 = {}
players2 = {}

count = 0
for each in db.odi.find({"$or":[{"team1":"India","team2":"Australia"},{"team1":"Australia","team2":"India"}]}):
    #if(each.get('winner') == "India"):
    if(each.get('bowl1')[0].get('team') == "India"):
        team1["team"] = "India"
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
                total = total + int(pl.get('wickets'))
                temp["wkt"] = total
                temp["nom"] = nom
                temp["eco"] = eco
                players1[str(pl.get('bowler'))] = temp
               
            else:
                bowl={} 
                bowl["wkt"] = int(pl.get('wickets'))
                bowl["eco"] = float(pl.get('economy'))
                bowl["nom"] = 1
                players1[str(pl.get('bowler'))] = bowl
        team2["team"] = "Australia"
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
                total = total + int(pl.get('wickets'))
                temp["wkt"] = total
                temp["nom"] = nom
                temp["eco"] = eco
                players2[str(pl.get('bowler'))] = temp
               
            else:
                bowl={} 
                bowl["wkt"] = int(pl.get('wickets'))
                bowl["nom"] = 1
                bowl["eco"] = float(pl.get('economy'))
                players2[str(pl.get('bowler'))] = bowl    
    else:
        team1["team"] = "India"
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
                total = total + int(pl.get('wickets'))
                temp["wkt"] = total
                temp["nom"] = nom
                temp["eco"] = eco
                players1[str(pl.get('bowler'))] = temp
               
            else:
                bowl={} 
                bowl["wkt"] = int(pl.get('wickets'))
                bowl["eco"] = float(pl.get('economy'))
                bowl["nom"] = 1
                players1[str(pl.get('bowler'))] = bowl
                
        team2["team"] = "Australia"
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
                total = total + int(pl.get('wickets'))
                temp["wkt"] = total
                temp["nom"] = nom
                temp["eco"] = eco
                players2[str(pl.get('bowler'))] = temp
               
            else:
                bowl={} 
                bowl["wkt"] = int(pl.get('wickets'))
                bowl["nom"] = 1
                bowl["eco"] = float(pl.get('economy'))
                players2[str(pl.get('bowler'))] = bowl       
    #print "*******************************************"
    
print each    
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

print team1
print team2

    
    