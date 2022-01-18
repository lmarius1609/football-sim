from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Football Championship Simulator'

def sublink():
   return 'This is a sub-page'
app.add_url_rule('/sublink', 'sublink', sublink)


if __name__ == '__main__':
	app.run()