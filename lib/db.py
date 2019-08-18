import pymysql

def getConn():
	conn = pymysql.connect(host='localhost',user='cnunoti',password='localhost',db='cnunoti')
	return conn