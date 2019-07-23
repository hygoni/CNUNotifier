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

def savingMySQL(NumList, TextList): #mySQL에 새 소식 저장하기
    global conn
    global cursor
    try:
        for i in range(len(NumList)):
            sql = "insert into cnu_com_notifier values ("+NumList[i]+", '"+TextList[i]+ "')"
            cursor.execute(sql)
            conn.commit()
    except:
        traceback.print_exc()
    return

def getFromDB(): #소식 번호만 리스트로 받아오기
    global conn
    global cursor
    try:
        sql = "select number, txt from cnu_com_notifier order by number desc"
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

def printNewNews(num): #num의 개수만큼 새 소식 받아오기
    global conn
    global cursor
    try:
        sql = "select * from cnu_com_notifier order by number desc"
        cursor.execute(sql)
        result_list=[]
        for i in range(num):
            result = cursor.fetchone()
            result_list += list(result)
    except:
        traceback.print_exc()
    return


def getLastFromWeb():
    html=urlopen("https://computer.cnu.ac.kr/computer/notice/bachelor.do?mode=list&&articleLimit=10&article.offset=0")
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




while True:
    newNumber, newTitle=getLastFromWeb() #웹에서 가져옴
    oldNumber, oldTitle=getFromDB() #DB에서 가져옴

    numOfNewNews=findNumOfNew(newNumber, oldNumber)
    if numOfNewNews is not 0:
        printNewNews(numOfNewNews)
        savingMySQL(newNumber[:numOfNewNews], newTitle[:numOfNewNews])
        for title in newTitle[:numOfNewNews]:
            sendMessage('cse', '[공지] 컴퓨터융합학부', title)
    time.sleep(10)
