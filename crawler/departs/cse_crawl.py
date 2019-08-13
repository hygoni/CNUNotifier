# -*- coding: utf-8 -*-


import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import traceback

import sys
sys.path.append('/home/ubuntu/CNUNotifier/lib')
from depart import *

conn = pymysql.connect(host='localhost',user='cnunoti',password='localhost',db='cnunoti')
cursor=conn.cursor()

CSE_BACHELOR = 'https://computer.cnu.ac.kr/computer/notice/bachelor.do'
CSE_NOTICE = 'https://computer.cnu.ac.kr/computer/notice/notice.do'
CSE_PROJECT = 'https://computer.cnu.ac.kr/computer/notice/project.do'
CSE_JOB = 'https://computer.cnu.ac.kr/computer/notice/job.do'
CSE_NEWS = 'https://computer.cnu.ac.kr/computer/notice/cse.do'

def escape_quote(str):
    return str.replace('\'', '\\\'')

def getRecordCounts(table):
    global conn
    global cursor

    sql = 'SELECT COUNT(*) from {}'.format(table)
    cursor.execute(sql)
    conn.commit()
    count = cursor.fetchone()[0]
    return count


def create_table(table):
    sql = 'CREATE TABLE IF NOT EXISTS {}(number int, txt text)'.format(table)
    cursor.execute(sql)
    conn.commit()

def savingMySQL(numList, textList, table):
    global conn
    global cursor

    textList = [escape_quote(text) for text in textList] #Quote escaping

    create_table(table)
    try:
        for i in range(len(numList)):
            sql = "insert into {} values ({}, '{}')".format(table, numList[i], textList[i])
            cursor.execute(sql)
            conn.commit()
    except:
        traceback.print_exc()
    return

def getLastFromDB(table, n): #소식 번호만 리스트로 받아오기
    create_table(table)
    print(n)
    global conn
    global cursor

    try:
        sql = "select number, txt from " + table + " order by number desc limit {}".format(n)
        cursor.execute(sql)
        text_list = []
        num_list = []
        for i in range(n):
            result = cursor.fetchone()
            print(result)
            text_list.append(result[1])
            num_list.append(int(result[0]))
    finally:
        traceback.print_exc()
    return num_list, text_list

def printNewNews(num, table): #num의 개수만큼 새 소식 받아오기
    create_table(table)
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
    return result_list


def getLastFromWeb(url, n):
    html=urlopen(url)
    bsObj=BeautifulSoup(html.read(),"html.parser")
    Num=bsObj.html.body.tbody.findAll("tr")
    numList=[]
    textList=[]
    linkList=[]
    for line in Num:
        while len(numList) < n:
            if '공지' in line.find("td",{"class":"b-num-box"}).get_text():
                break
            else:
                numList+=[int(line.find("td",{"class":"b-num-box"}).get_text().strip())]
                textList+=[line.find("div", {"class":"b-title-box"}).find('a').get_text().strip()]
                linkList += [url + line.find("div", {"class":"b-title-box"}).find('a').attrs['href']]
                break
    return (numList,textList, linkList)


def crawl_one(url, msgTitle, table):
    print('Crawling {}...'.format(msgTitle))
    #초기 세팅
    create_table(table)
    count = getRecordCounts(table)
    if count == 0:
        oldNumber, oldTitle, _ = getLastFromWeb(url, 5)
        savingMySQL(oldNumber, oldTitle, table)
        return

    #최신 글 개수 불러오기
    lastNumFromWeb = getLastFromWeb(url, 1)[0][0] 
    lastNumFromDB = getLastFromDB(table, 1)[0][0]
    new = abs(lastNumFromWeb - lastNumFromDB)
    print('새 소식 : {}개'.format(new))
    if new == 0:
        return

    newNumber, newTitle, newLink = getLastFromWeb(url, new) #웹에서 가져옴
    for i in range(len(newTitle)):
        sendMessage('cse', msgTitle, newTitle[i], newLink[i])
    savingMySQL(newNumber, newTitle, table)

def crawl_all():
    while True:
        try:
            crawl_one(CSE_BACHELOR, '[학사공지] - 컴퓨터융합학부', 'CSE_BACHELOR')
            crawl_one(CSE_PROJECT, '[사업단소식] - 컴퓨터융합학부', 'CSE_PROJECT')
            crawl_one(CSE_NOTICE, '[일반소식] - 컴퓨터융합학부', 'CSE_NOTICE')
            crawl_one(CSE_JOB, '[취업정보] - 컴퓨터융합학부', 'CSE_JOB')
            crawl_one(CSE_NEWS, '[학부소식] - 컴퓨터융합학부', 'CSE_NEWS')
            time.sleep(10)
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    crawl_all()
