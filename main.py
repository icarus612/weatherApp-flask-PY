from flask import Flask, render_template, url_for, request, redirect
import requests
import os
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_sslify import SSLify

app = Flask(__name__)
if 'DYNO' in os.environ: # only trigger SSLify if the app is running on Heroku
    sslify = SSLify(app)
Bootstrap(app)
fa = FontAwesome(app)

@app.route('/')
def index():
	error = request.args.get('error')
	return render_template('weather.html', weather=None, error=error)

@app.route('/weather')
def weather():
	city = request.args.get('city')
	state = request.args.get('state')
	country = request.args.get('country')
	unit = request.args.get('unit')
	if state:
		req = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&units={unit}&appid=da0cf3bb954fb7fd96d7095ca8c4cb5f').json()
	else:
		req = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&units={unit}&appid=da0cf3bb954fb7fd96d7095ca8c4cb5f').json()
	print(req['weather'])
	weather = req['weather'][0]
	temp = req['main']
	return render_template('weather.html', weather=weather, temp=temp, unit=unit, error=None)

@app.route('/get_weather', methods=['POST'])
def get_weather():
	try:
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		unit = request.form['unit-type']
		print(city, state)
		if city is "" or country is "":
			return redirect(url_for('index', error="You need a city and country."))
		else:
			return redirect(url_for('weather', city=city, country=country, state=state, unit=unit))
	except:
		return redirect(url_for('index'))

port = int(os.environ.get('PORT', 5000)) 
if __name__ == '__main__':
	app.run(threaded=True, debug=True, port=port)
	