# -*- encoding: utf-8 -*-
import pymysql
from pymysql import OperationalError
import sys
sys.path.append('.')
from firebase import *

conn = pymysql.connect('localhost', user='cnunoti', password='localhost', db='cnunoti')
cursor = conn.cursor()

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


def sendMessage(depart, title, body):
    tokenList = getUsersFromDepart(depart)
    
    for token in tokenList:
        js = JSONMake(token, title, body)
        response = send(js)
        if 'NotRegistered' in response:
            unregister(depart, token)
            print('Deleted token {} '.format(token))
        print(response)
        

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
    sendMessage('cse', '재헌띠', 'ㅎㅇㅎㅇ')
