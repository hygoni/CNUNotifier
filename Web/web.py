from flask import Flask, render_template, request, redirect
app = Flask(__name__)

def alert(message):


@app.route('/subscribeFrom'):
def mainPage():
	return render_template('./subscribe.html')

@app.route('/subscribe', methods = ['POST'])
def register():
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

