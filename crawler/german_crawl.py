# -*- encoding: utf-8 -*-
import sys, ssl
from selenium import webdriver
sys.path.append('../lib')
from crawler import *
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1000x1080')
options.add_argument('disable-gpu')

def getDriver():
  global options
  driver = webdriver.Chrome('../lib/chromedriver', chrome_options=options)
  return driver

class crawl_german(General):

    def __init__(self, url, subs_table, table, msgTitle):
      super().__init__(url, subs_table, table, msgTitle)

    def getLastFromWeb(self, n):
      global driver
      numList = []
      textList = []
      driver.get(self.url)
      
      bsObj = BeautifulSoup(driver.page_source, 'html.parser')
      trs = bsObj.findAll('tr', {'class' : 'pline4list'})
       
      for tr in trs:
        td = tr.select('td')
        if 'list4notice' in tr.attrs['class']:
          continue #공지사항이면 패스

        a = td[2].find('a')
        if (len(a.get_text()) > 0) and (len(numList) < n):
          link = 'https://german.cnu.ac.kr' + a.attrs['href']
          title = self.getTitle(link)
          num = int(td[0].get_text().strip())
          textList.append(title)
          numList.append(num)
      return (numList, textList)

    
    def getTitle(self, link):
      global driver
      driver.get(link)
      bsObj = BeautifulSoup(driver.page_source, 'html.parser')
      return bsObj.find('div', {'class' : 'read_title'}).get_text()
with getDriver() as driver:
  german = crawl_german('https://german.cnu.ac.kr/notice.brd?shell=/index.shell:419', 'german', 'GERMAN_NOTICE', '독어독문학과')
  while True:
    german.crawl()
    time.sleep(1)