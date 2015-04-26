import urllib2
from bs4 import BeautifulSoup
from dataBean import DataBean
import json

dataList = []
startPage=urllib2.urlopen("http://stats.espncricinfo.com/ci/content/records/307851.html")
years = {}
allLinks = {}
soup = BeautifulSoup(startPage.read())
