import pymysql
conn = pymysql.connect(host='localhost', user='cnunoti', password='localhost', db='cnunoti')
cursor = conn.cursor()
cursor.execute('SELECT count(*) FROM cse')
result = cursor.fetchone()[0]
print(result)

