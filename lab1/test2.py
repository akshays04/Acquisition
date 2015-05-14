import urllib2
from bs4 import BeautifulSoup
from dataBean import DataBean
from Batting import Batting
import json

dataList = []
battinginfo=[]
startPage=urllib2.urlopen("http://stats.espncricinfo.com/ci/content/records/307851.html")
years = {}
allLinks = {}
soup = BeautifulSoup(startPage.read())

for link in soup.find_all('a'):
    allLinks[link.get_text()] = "http://stats.espncricinfo.com/" + link.get('href')

for link in allLinks.keys() :
    if(link.isdigit()):
        if(int(link)>=2015 and int(link)<=2015): 
            years[link] = allLinks[link]
            '''print link,
            print "    ",
            print years[link]'''
            
            
for link in years.keys():
    yearPage=urllib2.urlopen(years[link])
    yearSoup = BeautifulSoup(yearPage.read())
    for row in yearSoup.find('table').find_all('tr') :
        temp = DataBean()
        temp.team1 = str(row.find_next('td').text)
        temp.team2 = str(row.find_next('td').find_next('td').text)
        temp.winner = str(row.find_next('td').find_next('td').find_next('td').text)
        temp.margin = str(row.find_next('td').find_next('td').find_next('td').find_next('td').text)
        temp.location = str(row.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text)
        temp.date = str(row.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text)
        temp.scorecardLink = "http://stats.espncricinfo.com" + str(row.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find('a').get('href'))
        temp.id = row.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').get_text()
        
        #temp.__str__()
        dataList.append(temp)

for link in dataList:
    #print link.id
    #print link.scorecardLink
    '''urlLink = urllib2.urlopen(link.scorecardLink);'''
    urlLink = urllib2.urlopen('http://www.espncricinfo.com/ci/engine/match/514035.html');
    
    scorecard = ' '
    #urlLink = urllib2.urlopen('http://www.espncricinfo.com/ci/engine/match/754751.html');
    urlSoup = BeautifulSoup(urlLink.read())
    #battingScoreCard = urlSoup.findAll('table',{'class':'batting-table innings'})
    #team1Batting=battingScoreCard[0];
    #team2Batting=battingScoreCard[1];
    #print team1Batting
    #bowlingScoreCard= urlSoup.findAll('table',{'class':'batting-table innings'})
    #team1Bowling=bowlingScoreCard[0];
    #team1Bowling=bowlingScoreCard[1];
    count=1;
    while count<len(urlSoup.findAll('table',{'class':'batting-table innings'})[0].findAll('tr')):
        print len(urlSoup.findAll('table',{'class':'batting-table innings'})[0].findAll('tr'))
        print count
        objBatting=Batting() 
        t= urlSoup.findAll('table',{'class':'batting-table innings'})[0].findAll('tr')[count]
        if not t.find_next('td').find_next('td').a:
            count=count+2;
            break
            
        objBatting.name= t.find_next('td').find_next('td').a.string
        objBatting.runs=t.find_next('td').find_next('td').find_next('td').find_next('td').string
        objBatting.balls=t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string
        objBatting.sr=t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string
        print objBatting.name +" "+objBatting.runs+" "+objBatting.balls+" "+objBatting.sr
        count=count+2;
        
    '''count=1;
    while count<=urlSoup.findAll('table',{'class':'batting-table innings'})[1].findAll('tr').count:
        objBatting=Batting() 
        t= urlSoup.findAll('table',{'class':'batting-table innings'})[0].findAll('tr')[count]
        objBatting.name= t.find_next('td').find_next('td').a.string
        objBatting.runs=t.find_next('td').find_next('td').find_next('td').find_next('td').string
        objBatting.balls=t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string
        objBatting.sr=t.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').string
        print objBatting.name +" "+objBatting.runs+" "+objBatting.balls+" "+objBatting.sr
        count=count+2;'''
        
    
    
    
    
    '''print urlSoup.findAll('table',{'class':'batting-table innings'})[1].findAll('tr')[1]
    print urlSoup.findAll('table',{'class':'batting-table innings'})[1].findAll('tr')[3]
    for t in urlSoup.findAll('table',{'class':'batting-table innings'})[1].findAll('tr'):
        objBatting=Batting()  
        print t.find_next('td').find_next('td').a.string
        print t.find_next('td').find_next('td').find_next('td').text
        #print t.find_next('td').find_next('td').a.string'''
        
    
    
        
    
    #for t in urlSoup.find_all('table'):
        #scorecard += str(t)
        
    #link.scorecard = scorecard
    #print battingScoreCard
    #print "Scoreard "+link.scorecard
    #battingTable=scorecard.find('table',{'class':'batting-table innings'});
    #print battingTable
    #print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    

newList = []    
for eachItem in dataList:
    newDict = {}
    for key,value in eachItem.__dict__.iteritems():
        newDict[key] = value
    newList.append(newDict)

print newList
    
with open("records.json", 'wb') as outfile:
    json.dump(newList, outfile)
    