from flask import Flask, render_template, request, redirect
from flask import url_for, Response, send_from_directory
import threading
import sys
sys.path.append('../lib')
from firebase import *
from depart import *
from rewrite import *
from db import *
from rfeed import *
import datetime

app = Flask(__name__)
supportedDeparts = ['cse', 'german', 'free', 'dorm', 'french']

@app.route('/')
def mainPage():
    return render_template('index.html')
@app.route('/subscribeForm')
def subscribeForm():
	return render_template('subscribe.html')

@app.route('/subscribe', methods = ['GET'])
def subscribe():
    global supportedDeparts
    token = request.args.get('token')
    depart = request.args.get('depart')

    if ( not token ) or ( not depart ):
        return redirect(url_for('subscribeForm'))

    data = JSONMake(token, 'VALIDATION CHECK', 'TEST')
    response = send(data)
    if 'Invalid' in response:
        print('Invalid Token')
    else:
        if depart in supportedDeparts:
            register(depart, token)

    return redirect(url_for('mainPage'))

@app.route('/firebase-messaging-sw.js')
def sw_js():
    js = render_template('firebase-messaging-sw.js')
    r = Response(response=js, status=200, mimetype='application/javascript')
    r.headers['Content-Type'] = 'text/javascript'
    return r

def make_rss(depart):
    conn = getConn()
    cursor = conn.cursor()
    if depart == 'dorm':
        sql = 'SELECT txt, link, time from DORM_NOTICE ORDER BY time DESC'
    elif depart == 'cse':
    	sql = '''SELECT txt, link, time FROM CSE_BACHELOR
    	UNION SELECT txt, link, time FROM CSE_JOB
    	UNION SELECT txt, link, time FROM CSE_NEWS
    	UNION SELECT txt, link, time FROM CSE_NOTICE
    	UNION SELECT txt, link, time FROM CSE_NOTICE_BACHELOR WHERE txt != 'Empty Notice'
    	UNION SELECT txt, link, time FROM CSE_NOTICE_JOB WHERE txt != 'Empty Notice'
    	UNION SELECT txt, link, time FROM CSE_NOTICE_NEWS WHERE txt != 'Empty Notice'
    	UNION SELECT txt, link, time FROM CSE_NOTICE_PROJECT WHERE txt != 'Empty Notice'
    	UNION SELECT txt, link, time FROM CSE_NOTICE_NOTICE WHERE txt != 'Empty Notice'
    	UNION SELECT txt, link, time FROM CSE_PROJECT ORDER BY time DESC'''

    cursor.execute(sql)
    conn.commit()
    item_list = []
    for row in cursor.fetchall():
        item = Item(
        title = row[0],
        link = row[1],
        description = "충대알리미가 알려주는 공지사항입니다!",
        author = depart,
        guid = Guid(row[1]),
        pubDate = datetime.datetime.fromtimestamp(row[2]))
        item_list.append(item)
    feed = Feed(
        title = "충남대 공지 RSS",
        link = "https://pansle.com/rss/" + depart,
        description = "충남대 공지 RSS",
        language = "ko-KR",
        lastBuildDate = datetime.datetime.now(),
        items = item_list)
    return feed.rss()



@app.route('/rss/<depart>')
def rss(depart):
    global supportedDeparts
    if depart in supportedDeparts:
        return make_rss(depart)
    else:
        return redirect(url_for('mainPage'))

rewrite = threading.Thread(target=startRewrite) #80port to 433port rewriter
rewrite.start()
context = ('/etc/letsencrypt/live/pansle.com/cert.pem', '/etc/letsencrypt/live/pansle.com/privkey.pem')
app.run(host='0.0.0.0', port = 443, ssl_context=context)
