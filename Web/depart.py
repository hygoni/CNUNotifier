import pymysql
import sys
sys.path.append('.')
from firebase import *

conn = pymysql.connect('localhost', user='cnunoti', password='localhost', db='cnunoti')
cursor = conn.cursor()


def getUsersFromDepart(depart):
    sql = 'SELECT * FROM {}'.format(depart)
    cursor.execute(sql)
    conn.commit()

    result = cursor.fetchall()
    result = [list(tup)[0] for tup in result]
    return result


def sendMessage(depart, title, body):
    tokenList = getUsersFromDepart(depart)
    
    for token in tokenList:
        js = JSONMake(token, title, body)
        print(send(js))

def register(depart, token):
    sql = "INSERT INTO {} (token) SELECT * FROM (SELECT '{}') AS tmp WHERE NOT EXISTS (SELECT token FROM cse WHERE token = '{}' ) LIMIT 1;".format(depart, token, token)
    cursor.execute(sql)
    conn.commit()


#register('cse', 'hitokenhello')
#getUsersFromDepart('cse')
sendMessage('cse', '긴급공지', 'halo')

