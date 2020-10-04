import pymysql

def getConn():
	conn = pymysql.connect(host='localhost', user='cnunoti', password='cnunoti', db='cnunoti')
	return conn
