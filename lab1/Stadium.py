import pymongo
import math
import json

client = pymongo.MongoClient("localhost", 27017)
db = client.CricStats
count = 0
sum=0

ourTeam = "Australia"
location = "Sydney"

numOfMatches = 0
batFirstWins = 0
batSecondWins = 0
ourTeamMatches = 0
ourTeamWins = 0
ourTeamB1Wins = 0
ourTeamB2Wins = 0
ourTeamAvgScoreB1 = 0
ourTeamAvgScoreB2 = 0
highestScore = 0
lowestScore = 0
avgScoreB1 = 0
avgScoreB2 = 0

highestScore = 0
lowestScore = 0

b1Score = 0
b1Count = 0
b2Score = 0
b2Count = 0

for each in db.odi.find({'location': { '$in': [location ] }}):
    numOfMatches = numOfMatches + 1
    
    '''highestScore Calc '''
    if int(each["team1 Total"])>int(each["team2 Total"]):
        if highestScore == 0:
            highestScore = int(each["team1 Total"])
        elif int(each["team1 Total"])>highestScore:
            highestScore = int(each["team1 Total"])
    else: 
        if highestScore == 0:
            highestScore = int(each["team2 Total"])
        elif int(each["team2 Total"])>highestScore:
            highestScore = int(each["team2 Total"])
            
    '''lowestScore Calc'''
    if int(each["team1 Total"])<int(each["team2 Total"]):
        if lowestScore == 0:
            lowestScore = int(each["team1 Total"])
        elif int(each["team1 Total"])<lowestScore:
            lowestScore = int(each["team1 Total"])
    else: 
        if lowestScore == 0:
            lowestScore = int(each["team1 Total"])
        elif int(each["team2 Total"])<lowestScore:
            lowestScore = int(each["team1 Total"])
        
    if(each.get('bat1')[0].get('team') == each.get('winner')):
        batFirstWins = batFirstWins + 1
    else:
        batSecondWins = batSecondWins + 1
    if(each.get('bat1')[0].get('team') == ourTeam or each.get('bat2')[0].get('team') == ourTeam):
        ourTeamMatches = ourTeamMatches + 1
        if (each.get('bat1')[0].get('team') == ourTeam or each.get('bat2')[0].get('team') == ourTeam) and each.get('winner') ==ourTeam : 
            ourTeamWins = ourTeamWins + 1
        if (each.get('bat1')[0].get('team') == ourTeam) and each.get('winner') ==ourTeam:
            ourTeamB1Wins = ourTeamB1Wins + 1
        if (each.get('bat2')[0].get('team') == ourTeam) and each.get('winner') ==ourTeam:
            ourTeamB2Wins = ourTeamB2Wins + 1
        if (each.get('bat1')[0].get('team') == ourTeam) and each.get('winner') ==ourTeam:
            b1Score = b1Score + int(each["team1 Total"])
            b1Count = b1Count + 1
        if (each.get('bat2')[0].get('team') == ourTeam) and each.get('winner') ==ourTeam:
            b2Score = b2Score + int(each["team2 Total"])
            b2Count = b2Count + 1
            
tempDict = {}
tempDict["numOfMatches"] = numOfMatches
tempDict["highestScore"] = highestScore
tempDict["lowestScore"] = lowestScore
tempDict["batFirstWins"] = batFirstWins
tempDict["batSecondWins"] = batSecondWins
tempDict["ourTeamMatches"] = ourTeamMatches
tempDict["ourTeamWins"] = ourTeamWins
tempDict["ourTeamB1Wins"] = ourTeamB1Wins
tempDict["ourTeamB2Wins"] = ourTeamB2Wins
tempDict["avgB1Win"] = b1Score / b1Count
tempDict["avgB2Win"] = b2Score / b2Count

print tempDict

with open('stadium.json', 'w') as outfile:
    json.dump(tempDict, outfile)

        
    