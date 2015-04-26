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
