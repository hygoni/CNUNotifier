# -*- encoding: utf-8 -*-
import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import traceback

import sys
sys.path.append('../lib')
from depart import *

conn = pymysql.connect(host='localhost',user='cnunoti',password='localhost',db='cnunoti')
cursor=conn.cursor()

class NotOverridedError(Exception):
	def __init__(self, funcName):
		super().__init__('{} 함수를 오버라이딩 하지 않았습니다!'.format(funcName))

class GeneralNoNum(General):


class General():
	def __init__(self, url, subs_table, table, msgTitle):
		self.url = url
		self.subs_table = subs_table
		self.table = table
		self.msgTitle = msgTitle

	def escape_quote(self, str):
		return str.replace('\'', '\\\'')

	def getRecordCounts(self):
		global conn
		global cursor

		sql = 'SELECT COUNT(*) from {}'.format(self.table)
		cursor.execute(sql)
		conn.commit()
		count = cursor.fetchone()[0]
		return count


	def create_table(self):
		sql = 'CREATE TABLE IF NOT EXISTS {}(number int, txt text)'.format(self.table)
		cursor.execute(sql)
		conn.commit()

	def savingMySQL(self, NumList, TextList): #mySQL에 새 소식 저장하기
		global conn
		global cursor

		TextList = [self.escape_quote(text) for text in TextList] #Quote escaping

		self.create_table()
		try:
			for i in range(len(NumList)):
				sql = "insert into {} values ({}, '{}')".format(self.table, NumList[i], TextList[i])
				cursor.execute(sql)
				conn.commit()
		except:
			traceback.print_exc()
		return

	def getLastFromDB(self, n): #소식 번호만 리스트로 받아오기
		self.create_table()
		print(n)
		global conn
		global cursor

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
		finally:
			traceback.print_exc()
		return num_list, text_list


	def getLastFromWeb(self, n): #자식에서 재정의해야함, return type : (num_list, text_list) (tuple)
		raise NotOverridedError('getLastFromWeb()')

	def crawl(self):
		print('Crawling {}...'.format(self.msgTitle))
		#초기 세팅
		self.create_table()
		count = self.getRecordCounts()
		if count == 0:
			oldNumber, oldTitle = self.getLastFromWeb(5)
			self.savingMySQL(oldNumber, oldTitle)
			return

		#최신 글 개수 불러오기
		lastNumFromWeb = self.getLastFromWeb(1)[0][0] 
		lastNumFromDB = self.getLastFromDB(1)[0][0]
		new = abs(lastNumFromWeb - lastNumFromDB)
		print(lastNumFromDB, lastNumFromWeb)
		print('새 소식 : {}개'.format(new))
		if new == 0:
			return

		newNumber, newTitle = self.getLastFromWeb(new) #웹에서 가져옴

		for articleTitle in newTitle:
			sendMessage(self.subs_table, self.msgTitle, articleTitle)
			self.savingMySQL(newNumber, newTitle)
