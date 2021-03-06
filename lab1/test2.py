import urllib2
from bs4 import BeautifulSoup
from dataBean import DataBean
from Batting import Batting
from Bowling import Bowling

import pymongo

mainArr = []

dataList = []
battinginfo=[]
startPage=urllib2.urlopen("http://stats.espncricinfo.com/ci/content/records/307851.html")
years = {}
allLinks = {}
soup = BeautifulSoup(startPage.read())
client = pymongo.MongoClient("localhost", 27017)
db = client.CricStats

for link in soup.find_all('a'):
    allLinks[link.get_text()] = "http://stats.espncricinfo.com/" + link.get('href')

for link in allLinks.keys() :
    if(link.isdigit()):
        if(int(link)>=2005 and int(link)<=2009): 
            years[link] = allLinks[link]
            
            
            
for link in years.keys():
    yearPage=urllib2.urlopen(years[link])
    yearSoup = BeautifulSoup(yearPage.read())
    for row in yearSoup.find('table').find_all('tr') :
        temp = DataBean()
        temp2 = {}
        temp.team1 = str(row.find_next('td').text)
        temp2["team1"] = str(row.find_next('td').text)
        temp.team2 = str(row.find_next('td').find_next('td').text)
        temp2["team2"] = str(row.find_next('td').find_next('td').text)
        temp.winner = str(row.find_next('td').find_next('td').find_next('td').text)
        temp2["winner"] = str(row.find_next('td').find_next('td').find_next('td').text)
        temp.margin = str(row.find_next('td').find_next('td').find_next('td').find_next('td').text)
        temp2["margin"] = str(row.find_next('td').find_next('td').find_next('td').find_next('td').text)
        temp.location = str(row.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text)
        temp2["location"] = str(row.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text)
        temp.date = str(row.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text)
        temp2["date"] = str(row.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text)
        temp.scorecardLink = "http://stats.espncricinfo.com" + str(row.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('href'))
        temp.id = row.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').get_text()
        
        '''
        new code start
        '''
        urlLink = urllib2.urlopen(temp.scorecardLink);
        
        scorecard = ' '
        bat1 = []
        bat2 = []
        bowl1 = []
        bowl2 = []
        
        urlSoup = BeautifulSoup(urlLink.read())
        
        count=1;
        #print temp.scorecardLink
        if temp2["winner"] != "no result":
            #print temp.scorecardLink
            total= str(urlSoup.findAll('table',{'class':'batting-table innings'})[0].find('tr',{'class':'total-wrap'}).find_all('td')[3].text)
            #print 'Team 1 total '+total
            temp2["team1 Total"] = total
            while count<len(urlSoup.findAll('table',{'class':'batting-table innings'})[0].findAll('tr')):
                tempBat = {}
                objBatting=Batting() 
                headerline= str(urlSoup.findAll('table',{'class':'batting-table innings'})[0].findAll('tr')[0].find('th',{'class':'th-innings-heading'}).text)
        
                tempBat["team"] = headerline.split(' ')[0]
                firstBatTeam = headerline.split(' ')[0]
                t= urlSoup.findAll('table',{'class':'batting-table innings'})[0].findAll('tr')[count]
                if not t.find_next('td').find_next('td').a:
                    count=count+2;
                    break
            
                objBatting.name= str(t.find_next('td').find_next('td').a.string)
                tempBat["batsman"] = str(t.find_next('td').find_next('td').a.string)
                objBatting.runs=str(t.find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBat["runs"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').string)
                objBatting.balls=str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBat["balls"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                objBatting.sr=str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBat["sr"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
        
                count=count+2;
                bat1.append(tempBat)
                
            count=1;
            if firstBatTeam == temp2["team1"]:
                secondBatTeam = temp2["team2"]
            else:
                secondBatTeam = temp2["team1"]
            #print temp.scorecardLink
            total= str(urlSoup.findAll('table',{'class':'batting-table innings'})[1].find('tr',{'class':'total-wrap'}).find_all('td')[3].text)
            #print 'Team 2 total '+total
            temp2["team2 Total"] = total
            while count<len(urlSoup.findAll('table',{'class':'batting-table innings'})[1].findAll('tr')):
                tempBat = {}
                objBatting=Batting() 
                t= urlSoup.findAll('table',{'class':'batting-table innings'})[1].findAll('tr')[count]
                if not t.find_next('td').find_next('td').a:
                    count=count+2;
                    break
                objBatting.name= str(t.find_next('td').find_next('td').a.string)
                tempBat["team"] = secondBatTeam
                tempBat["batsman"] = str(t.find_next('td').find_next('td').a.string)
                objBatting.runs=str(t.find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBat["runs"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').string)
                objBatting.balls=str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBat["balls"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                objBatting.sr=str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBat["sr"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                count=count+2;
                bat2.append(tempBat)
            
            count=1;
            while count<len(urlSoup.findAll('table',{'class':'bowling-table'})[0].findAll('tr')):
                tempBowl = {}
                objBowling=Bowling() 
                t= urlSoup.findAll('table',{'class':'bowling-table'})[0].findAll('tr')[count]
                tempBowl["team"] = secondBatTeam
                if not t.find_next('td').find_next('td').a:
                    count=count+2;
                    break
                objBowling.name= str(t.find_next('td').find_next('td').a.string)
                tempBowl["bowler"] = str(t.find_next('td').find_next('td').a.string)
                objBowling.overs=str(t.find_next('td').find_next('td').find_next('td').string)
                tempBowl["overs"] = str(t.find_next('td').find_next('td').find_next('td').string)
                objBowling.maidens=str(t.find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBowl["maidens"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').string)
                objBowling.runs=str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBowl["runsGiven"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                objBowling.wickets=str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBowl["wickets"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                objBowling.economy=str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBowl["economy"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
        
                count=count+2;
                bowl1.append(tempBowl)
                
            
            count=1;
            while count<len(urlSoup.findAll('table',{'class':'bowling-table'})[1].findAll('tr')):
                tempBowl = {}
                objBowling=Bowling() 
                t= urlSoup.findAll('table',{'class':'bowling-table'})[1].findAll('tr')[count]
                tempBowl["team"] = firstBatTeam
                if not t.find_next('td').find_next('td').a:
                    count=count+2;
                    break
                objBowling.name= str(t.find_next('td').find_next('td').a.string)
                tempBowl["bowler"] = str(t.find_next('td').find_next('td').a.string)
                objBowling.overs=str(t.find_next('td').find_next('td').find_next('td').string)
                tempBowl["overs"] = str(t.find_next('td').find_next('td').find_next('td').string)
                objBowling.maidens=str(t.find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBowl["maidens"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').string)
                objBowling.runs=str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBowl["runsGiven"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                objBowling.wickets=str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBowl["wickets"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                objBowling.economy=str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
                tempBowl["economy"] = str(t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string)
            
                count=count+2;
                bowl2.append(tempBowl)
                
            temp2["bat1"] = bat1
            temp2["bowl1"] = bowl1
            temp2["bat2"] = bat2
            temp2["bowl2"] = bowl2
            
            #print temp2
            mainArr.append(temp2)
            db.odi.insert_one(temp2).inserted_id
            
            
            
            
            '''
            new code end
            '''
            
            
            dataList.append(temp)



    