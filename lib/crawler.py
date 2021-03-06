# -*- encoding: utf-8 -*-
import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import traceback
 
import sys
import os
sys.path.append(os.environ['NOTI_PATH'] + '/lib')
from depart import *

def getConn():
	conn = pymysql.connect(host='localhost',user='cnunoti',password='localhost',db='cnunoti')
	return conn

class NotOverridedError(Exception):

	def __init__(self, funcName):
		super().__init__('{} 함수를 오버라이딩 하지 않았습니다!'.format(funcName))

class GeneralNoNum():

	def __init__(self, url, subs_table, table, msgTitle):
		self.url = url
		self.subs_table = subs_table
		self.table = table
		self.msgTitle = msgTitle

	def escape_quote(self, str):
		return str.replace('\'', '\\\'')

	def getRecordCounts(self):
		conn = getConn()
		cursor = conn.cursor()

		sql = 'SELECT COUNT(*) from {}'.format(self.table)
		cursor.execute(sql)
		conn.commit()
		count = cursor.fetchone()[0]
		conn.close()
		return int(count)


	def create_table(self):
		sql = 'CREATE TABLE IF NOT EXISTS {}(txt text, link text, time double)'.format(self.table)
		conn = getConn()
		cursor.execute(sql)
		conn.commit()


		if(self.getRecordCounts() == 0):
			sql = 'INSERT INTO {} VALUES(\'EMPTY NOTICE\', \'https://pansle.com\',  {})'.format(self.table, time.time())
			cursor.execute(sql)
			conn.commit()

		conn.close()

	def savingMySQL(self, TextList, linkList, timeList): #mySQL에 새 소식 저장하기
		conn = getConn()
		cursor = conn.cursor()

		TextList = [self.escape_quote(text) for text in TextList] #Quote escaping
		linkList = [self.escape_quote(link) for link in linkList]
		self.create_table()
		try:
			for i in range(len(TextList)):
				sql = "insert into {} values ('{}', '{}', {})".format(self.table, TextList[i], linkList[i], timeList[i])
				cursor.execute(sql)
				conn.commit()
		except:
			traceback.print_exc()

		conn.close()
		return

	def isInDB(self, title): #소식 번호만 리스트로 받아오기
		conn = getConn()
		cursor = conn.cursor()
		title = self.escape_quote(title)

		try:
			sql = "select count(*) from " + self.table + " where txt = '{}' ".format(title)
			cursor.execute(sql)
			text_list = []
			count = int(cursor.fetchone()[0])
			return count
		except:
			traceback.print_exc()
			return 1

		conn.close()

	def getLastFromWeb(self): #자식에서 재정의해야함, return type : text_list
		raise NotOverridedError('getLastFromWeb()')

	async def crawl(self, channel):
		print('Crawling {}...'.format(self.msgTitle))
		#초기 세팅
		self.create_table()
		count = self.getRecordCounts()
		if count == 0:
			oldTitle, oldLink, oldTime = self.getLastFromWeb()
			self.savingMySQL(oldTitle, oldLink, oldTime)
			return
		newTitle, newLink, newTime = self.getLastFromWeb() #웹에서 가져옴
		for i in range(len(newTitle)):
			await sendMessage(self.subs_table, self.msgTitle, newTitle[i], newLink[i], channel)
			self.savingMySQL(newTitle, newLink, newTime)

class General():
	def __init__(self, url, subs_table, table, msgTitle):
		self.url = url
		self.subs_table = subs_table
		self.table = table
		self.msgTitle = msgTitle

	def escape_quote(self, str):
		return str.replace('\'', '\\\'')

	def getRecordCounts(self):
		conn = getConn()
		cursor = conn.cursor()

		sql = 'SELECT COUNT(*) from {}'.format(self.table)
		cursor.execute(sql)
		conn.commit()
		count = cursor.fetchone()[0]
		conn.close()
		return count


	def create_table(self):
		conn = getConn()
		cursor = conn.cursor()
		sql = 'CREATE TABLE IF NOT EXISTS {}(number int, txt text, link text, time double)'.format(self.table)
		cursor.execute(sql)
		conn.commit()
		conn.close()

	def savingMySQL(self, NumList, TextList, linkList, timeList): #mySQL에 새 소식 저장하기
		conn = getConn()
		cursor = conn.cursor()

		TextList = [self.escape_quote(text) for text in TextList] #Quote escaping
		linkList = [self.escape_quote(link) for link in linkList]
		self.create_table()
		try:
			for i in range(len(NumList)):
				sql = "insert into {} values ({}, '{}', '{}', {})".format(self.table, NumList[i], TextList[i], linkList[i], timeList[i])
				cursor.execute(sql)
				conn.commit()
		except:
			traceback.print_exc()
		conn.close()
		return

	def getLastFromDB(self, n): #소식 번호만 리스트로 받아오기
		self.create_table()
		print(n)
		conn = getConn()
		cursor = conn.cursor()
		try:
			sql = "select number, txt from " + self.table + " order by number desc limit {}".format(n)
			cursor.execute(sql)
			text_list = []
			num_list = []
			for i in range(n):
				result = cursor.fetchone()
				print(result)
				text_list.append(result[1])
				num_list.append(int(result[0]))
		except:
			traceback.print_exc()

		conn.close()
		return num_list, text_list


	def getLastFromWeb(self, n): #자식에서 재정의해야함, return type : (num_list, text_list) (tuple)
		raise NotOverridedError('getLastFromWeb()')

	async def crawl(self, channel):
		print('Crawling {}...'.format(self.msgTitle))
		#초기 세팅
		self.create_table()
		count = self.getRecordCounts()
		if count == 0:
			oldNumber, oldTitle, oldLink, oldTime = self.getLastFromWeb(5)
			self.savingMySQL(oldNumber, oldTitle, oldLink, oldTime)
			return
		#최신 글 개수 불러오기
		lastNumFromWeb = self.getLastFromWeb(1)[0][0] 
		lastNumFromDB = self.getLastFromDB(1)[0][0]
		new = abs(lastNumFromWeb - lastNumFromDB)
		print('새 소식 : {}개'.format(new))
		if new == 0:
			return
		newNumber, newTitle, newLink, newTime = self.getLastFromWeb(new) #웹에서 가져옴
		for i in range(len(newTitle)):
			await sendMessage(self.subs_table, self.msgTitle, newTitle[i], newLink[i], channel)
			self.savingMySQL(newNumber, newTitle, newLink, newTime)
