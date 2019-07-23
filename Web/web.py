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

app.run(host='0.0.0.0', port = 81)
