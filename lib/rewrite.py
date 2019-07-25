from flask import Flask, redirect
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def rewrite(path):
    return redirect('https://pansle.com/' + path)

def startRewrite():
    app.run(host='0.0.0.0', port = 80)

if __name__ == '__main__':
    startRewrite()
