from flask import Flask, render_template, request, redirect
from flask import url_for

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

@app.route('/token/<value>')
def token(value):
    sendMessage(value, 'Thanks for your subscription!')
    return value

def sendMessage(token_val, message):
    import os
    os.system('curl -X POST --header "Authorization: key=AAAADTgtg7E:APA91bHDBxYW9AEJT1BnDwbitDLrt1PnTCuwn_vuI8zHcaal8dpZ7YFj7DAgeVBxvLkVCPlFalvHJIWNvTbQiW5CsmCMBzty_1VIQpJaDvS0v71IbRUAnZbUvFeOIahbw36EJDRgsTHk"     --Header "Content-Type: application/json"     https://fcm.googleapis.com/fcm/send     -d "{\"to\":\"' + token_val + '\",\"notification\":{\"body\":\"' + message + '"\"}}"')

app.run(host='0.0.0.0', port = 81)
