# -*- encoding: utf-8 -*-

import pymysql
from pymysql import OperationalError
import sys
import os
sys.path.append(os.environ['NOTI_PATH'] + '/lib')

conn = pymysql.connect('localhost', user='cnunoti', password='localhost', db='cnunoti')
cursor = conn.cursor()

CHANNEL = ''

def reconnect():
    print('OperationalError Occurred, reconnecting mysql...')
    global conn
    global cursor

    conn = pymysql.connect('localhost', user='cnunoti', password='localhost', db='cnunoti')
    cursor = conn.cursor()
    print('Reconnect completed.')

def getUsersFromDepart(depart):
    try:
        sql = 'SELECT * FROM {}'.format(depart)
        cursor.execute(sql)
        conn.commit()
    except OperationalError:
        reconnect()
        return getUserFromDepart(depart)

    result = cursor.fetchall()
    result = [list(tup)[0] for tup in result]
    return result


async def sendMessage(depart, title, body, link, channel):
	await channel.send(depart + ' ' + title)
	await channel.send(body)
	await channel.send(link)

def register(depart, token):
    try:
        sql = "INSERT INTO {} (token) SELECT * FROM (SELECT '{}') AS tmp WHERE NOT EXISTS (SELECT token FROM {} WHERE token = '{}' ) LIMIT 1;".format(depart, token, depart, token)
        print(sql)
        cursor.execute(sql)
        conn.commit()
    except:
        reconnect()
        register(depart, token)

def unregister(depart, token):
    try:
        sql = "DELETE FROM {} WHERE token = '{}'".format(depart, token)
        cursor.execute(sql)
        conn.commit()
    except:
        reconnect()
        unregister(depart, token)

#register('cse', 'hitokenhello')
#getUsersFromDepart('cse')
#register('cse', 'helloWorld')
#print(getUsersFromDepart('cse'))
#sendMessage('cse', '제목', '내용')
if __name__ == '__main__':
    sendMessage('cse', '충대알리미 오류 안내', '오늘 11시경에 오류가 발생해 메시지가 반복적으로 전송되었습니다. 현재 버그는 해결된 상태입니다. 감사합니다.', 'https://pansle.com')
