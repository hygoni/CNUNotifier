from flask import Flask, render_template, request, redirect
from flask import url_for, Response
import sys
sys.path.append('.')
from firebase import *
from depart import *

app = Flask(__name__)

def alert(msg):
    return '<script>alert("{}");</script>'.format(msg)

@app.route('/')
def mainPage():
    return redirect(url_for('subscribeForm'))

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


context = ('/etc/letsencrypt/live/deepnetworks.net/cert.pem', '/etc/letsencrypt/live/deepnetworks.net/privkey.pem')
app.run(host='0.0.0.0', port = 82, ssl_context=context)
