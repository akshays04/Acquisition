import urllib2
from bs4 import BeautifulSoup
from dataBean import DataBean
import json

dataList = []
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
    urlLink = urllib2.urlopen(link.scorecardLink);
    
    scorecard = ' '
    #urlLink = urllib2.urlopen('http://www.espncricinfo.com/ci/engine/match/754751.html');
    urlSoup = BeautifulSoup(urlLink.read())
    #abc=urlSoup.find('table',{'class':'batting-table innings'})
    for t in urlSoup.find_all('table'):
        scorecard += str(t)
        
    link.scorecard = scorecard
    #print abc
    #print link.scorecard
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
    