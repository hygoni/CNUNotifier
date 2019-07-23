import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import traceback

import sys
sys.path.append('.')
from depart import *

conn = pymysql.connect(host='localhost',user='cnunoti',password='localhost',db='cnunoti')
cursor=conn.cursor()

CSE_BACHELOR = 'https://computer.cnu.ac.kr/computer/notice/bachelor.do'
CSE_NOTICE = 'https://computer.cnu.ac.kr/computer/notice/notice.do'
CSE_PROJECT = 'https://computer.cnu.ac.kr/computer/notice/project.do'
CSE_JOB = 'https://computer.cnu.ac.kr/computer/notice/job.do'
CSE_NEWS = 'https://computer.cnu.ac.kr/computer/notice/cse.do'

def savingMySQL(NumList, TextList, table): #mySQL에 새 소식 저장하기
    global conn
    global cursor
    try:
        for i in range(len(NumList)):
            sql = "insert into " + table + " values ("+NumList[i]+", '"+TextList[i]+ "')"
            cursor.execute(sql)
            conn.commit()
    except:
        traceback.print_exc()
    return

def getFromDB(table): #소식 번호만 리스트로 받아오기
    global conn
    global cursor
    try:
        sql = "select number, txt from " + table + " order by number desc"
        cursor.execute(sql)
        text_list = []
        num_list = []
        for i in range(5):
            result = cursor.fetchone()
            print(result)
            text_list.append(result[1])
            num_list.append(int(result[0]))
    finally:
        traceback.print_exc()
    return num_list, text_list

def printNewNews(num, table): #num의 개수만큼 새 소식 받아오기
    global conn
    global cursor
    try:
        sql = "select * from " + table +" order by number desc"
        cursor.execute(sql)
        result_list=[]
        for i in range(num):
            result = cursor.fetchone()
            result_list += list(result)
    except:
        traceback.print_exc()
    return


def getLastFromWeb(url):
    html=urlopen(url)
    bsObj=BeautifulSoup(html.read(),"html.parser")
    Num=bsObj.html.body.tbody.findAll("tr")
    NumList=[]
    TextList=[]
    for line in Num:
        while len(NumList)<5:
            if '공지' in line.find("td",{"class":"b-num-box"}).get_text():
                break
            else:
                NumList+=[line.find("td",{"class":"b-num-box"}).get_text().strip()]
                TextList+=[line.find("div", {"class":"b-title-box"}).find('a').get_text().strip()]
                break
    return (NumList,TextList)

def findNumOfNew(NewList, OldList):
    if NewList[0]==OldList[0]:#List1이 새거
        print('새로운 소식이 없습니다')
        return 0
    else:
        News=str((int)(NewList[0])-(int)(OldList[0]))
        print('새로운 소식이 '+News+'개 있습니다.')
        return int(News)




def crawl_one(url, msgTitle, table):
    newNumber, newTitle=getLastFromWeb(url) #웹에서 가져옴
    oldNumber, oldTitle=getFromDB(table) #DB에서 가져옴

    numOfNewNews=findNumOfNew(newNumber, oldNumber)
    if numOfNewNews is not 0:
        printNewNews(numOfNewNews, table)
        savingMySQL(newNumber[:numOfNewNews], newTitle[:numOfNewNews], table)
        for articleTitle in newTitle[:numOfNewNews]:
            sendMessage('cse', msgTitle, articleTitle)

def crawl_all():
	while True:
		crawl_one(CSE_BACHELOR, '[학사공지] - 컴퓨터융합학부', 'CSE_BACHELOR')
		crawl_one(CSE_PROJECT, '[사업단소식] - 컴퓨터융합학부', 'CSE_PROJECT')
		crawl_one(CSE_NOTICE, '[일반소식] - 컴퓨터융합학부', 'CSE_NOTICE')
		crawl_one(CSE_JOB, '[취업정보] - 컴퓨터융합학부', 'CSE_JOB')
		crawl_one(CSE_NEWS, '[학부소식] - 컴퓨터융합학부', 'CSE_NEWS')
		time.sleep(10)