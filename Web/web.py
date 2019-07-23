from flask import Flask, render_template, request, redirect
from flask import url_for, Response
import sys
sys.path.append('.')
from firebase import *

app = Flask(__name__)

@app.route('/')
def mainPage():
    return redirect(url_for('subscribeForm'))

@app.route('/subscribeForm')
def subscribeForm():
	return render_template('subscribe.html')

@app.route('/subscribe', methods = ['POST'])
def subscribe():
	data = request.form
	if not data['id']:
		return redirect(url_for('subscribeForm'), code = 302)
	elif not data['password']:
		return redirect(url_for('subscribeForm'), code = 302)
	elif not data['depart']:
		return redirect(url_for('subscribeForm'), code = 302)
	elif not data['email']:
		return redirect(url_for('subscribeForm'), code = 302)

	return 'Success!'

@app.route('/fire')
def fire():
    return render_template('fire.html')

@app.route('/token')
def token():
    value = request.args.get('value')
    depart = request.args.get('depart')
    
    if value == None:
        return 'no token value'
    elif depart == None:
        return 'no depart'

    data = JSONMake(value, 'VALIDATION CHECK', 'TEST')
    txt = send(data)
    if 'Invalid' in txt:
        print('invalid token')
    else:
        print('nothing')
    #sendMessage(value, 'Thanks for your subscription!')
    return value


@app.route('/firebase-messaging-sw.js')
def sw_js():
    js = render_template('firebase-messaging-sw.js')
    r = Response(response=js, status=200, mimetype='application/javascript')
    r.headers['Content-Type'] = 'text/javascript'
    return r


context = ('/etc/letsencrypt/live/deepnetworks.net/cert.pem', '/etc/letsencrypt/live/deepnetworks.net/privkey.pem')
app.run(host='0.0.0.0', port = 82, ssl_context=context)
