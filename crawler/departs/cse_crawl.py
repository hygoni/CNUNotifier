# -*- coding: utf-8 -*-

import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import traceback
import pdb

import sys
sys.path.append('../../lib')
from depart import *
from crawler import *

CSE_BACHELOR = 'https://computer.cnu.ac.kr/computer/notice/bachelor.do'
CSE = 'https://computer.cnu.ac.kr/computer/notice/notice.do'
CSE_PROJECT = 'https://computer.cnu.ac.kr/computer/notice/project.do'
CSE_JOB = 'https://computer.cnu.ac.kr/computer/notice/job.do'
CSE_NEWS = 'https://computer.cnu.ac.kr/computer/notice/cse.do'

class CSE(GeneralNoNum):
    def __init__(self, url, subs_table, table, msgTitle):
        super().__init__(url, subs_table, table, msgTitle)

    def getLastFromWeb(self):
        html=urlopen(self.url)
        bsObj=BeautifulSoup(html.read(),"html.parser")
        Num=bsObj.html.body.tbody.findAll("tr")
        #numList=[]
        textList=[]
        linkList=[]
        timeList =[]
        for line in Num:
            #numList+=[int(line.find("td",{"class":"b-num-box"}).get_text().strip())]
            title = line.find("div", {"class":"b-title-box"}).find('a').get_text().strip()
            if self.isInDB(title) != 0:
                continue
            textList += [title]
            linkList += [self.url + line.find("div", {"class":"b-title-box"}).find('a').attrs['href']]
            timeList += [time.time()]
        return textList, linkList, timeList

bachelor = CSE('https://computer.cnu.ac.kr/computer/notice/bachelor.do', 'cse', 'CSE_BACHELOR', '[학사공지] - 컴퓨터융합학부')
project = CSE('https://computer.cnu.ac.kr/computer/notice/project.do', 'cse', 'CSE_PROJECT', '[사업단소식] - 컴퓨터융합학부')
job = CSE('https://computer.cnu.ac.kr/computer/notice/job.do', 'cse', 'CSE_JOB', '[취업정보] - 컴퓨터융합학부')
news = CSE('https://computer.cnu.ac.kr/computer/notice/cse.do', 'cse', 'CSE_NEWS', '[학부소식] - 컴퓨터융합학부')
general = CSE('https://computer.cnu.ac.kr/computer/notice/notice.do', 'cse', 'CSE_NOTICE', '[일반소식] - 컴퓨터융합학부')

def crawl_all():
    #pdb.set_trace()
    bachelor.crawl()
    project.crawl()
    job.crawl()
    news.crawl()
    general.crawl()                

if __name__ == '__main__':
    crawl_all()
