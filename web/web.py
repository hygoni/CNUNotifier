from flask import Flask, render_template, request, redirect
from flask import url_for, Response, send_from_directory
import threading
import sys
sys.path.append('../lib')
from firebase import *
from depart import *
from rewrite import *

app = Flask(__name__)

@app.route('/')
def mainPage():
    return render_template('index.html')
@app.route('/subscribeForm')
def subscribeForm():
	return render_template('subscribe.html')

@app.route('/subscribe', methods = ['GET'])
def subscribe():
    token = request.args.get('token')
    depart = request.args.get('depart')

    if ( not token ) or ( not depart ):
        return redirect(url_for('subscribeForm'))

    data = JSONMake(token, 'VALIDATION CHECK', 'TEST')
    response = send(data)
    if 'Invalid' in response:
        print('Invalid Token')
    else:
        if depart in ['cse']:
            register(depart, token)

    return redirect(url_for('mainPage'))

@app.route('/firebase-messaging-sw.js')
def sw_js():
    js = render_template('firebase-messaging-sw.js')
    r = Response(response=js, status=200, mimetype='application/javascript')
    r.headers['Content-Type'] = 'text/javascript'
    return r

rewrite = threading.Thread(target=startRewrite) #80port to 433port rewriter
rewrite.start()
context = ('/etc/letsencrypt/live/pansle.com/cert.pem', '/etc/letsencrypt/live/pansle.com/privkey.pem')
app.run(host='0.0.0.0', port = 443, ssl_context=context)
