# -*- coding: utf-8 -*-

import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import traceback

import sys
sys.path.append('../../lib')
from depart import *
from crawler import *

class French(General):
    def __init__(self, url, subs_table, table, msgTitle):
        super().__init__(url, subs_table, table, msgTitle)

    def getLastFromWeb(self, n):
        html=urlopen(self.url)
        bsObj=BeautifulSoup(html.read(),"html.parser")
        numList=[]
        textList=[]
        linkList=[]

        notice_num = bsObj.findAll("td",{"class":"b-num-box"})
        notice_link = bsObj.findAll("div", {"class":"b-title-box"})
        notice_text = bsObj.findAll("div", {"class":"b-title-box"})

        for i in notice_num:
            numList.append(int(i.get_text().strip()))
        for i in notice_link:
            linkList.append(self.url + i.find('a').attrs['href'])
        for i in notice_text:
            textList.append(i.find('a').get_text().strip())
        timeList = [time.time() for i in numList]
        return numList[:n],textList[:n], linkList[:n], timeList[:n]
 
french = French('https://french.cnu.ac.kr/french/community/notice-under.do', 'french', 'FRENCH_NOTICE', '불어불문학과')

def crawl_all():
    french.crawl()            

if __name__ == '__main__':
    crawl_all()
