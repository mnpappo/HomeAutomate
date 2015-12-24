from flask import Flask, flash, render_template, request, abort, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import RPi.GPIO as GPIO

app = Flask(__name__)

#db configs
app.config.from_pyfile('db.cfg')
db = SQLAlchemy(app)

#import models
from models import *

#pin setups
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
led = 4
pinList = [2, 3, led]
for i in pinList:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.LOW)


#####--Controllers---########
@app.route('/')
def home():
	return render_template('home.html')

#led
@app.route('/led_on/')
def led_on():
	GPIO.setup(led, GPIO.IN)
	state = GPIO.input(led)
	if state:
		print("LED is already ON state!")
		GPIO.setup(led, GPIO.OUT)
		return render_template('home.html')
	else:
		GPIO.setup(led, GPIO.OUT)
		GPIO.output(led,1)
		print("LED ON")
		return render_template('home.html')
	return render_template('home.html')

@app.route('/led_off/')
def led_off():
	GPIO.setup(led, GPIO.IN)
	state = GPIO.input(led)
	if state:
		GPIO.setup(led, GPIO.OUT)
		GPIO.output(led,0)
		print("LED OFF")
		return render_template('home.html')
	else:
		print("LED is already OFF state!")
		return render_template('home.html')
	return render_template('home.html')

#relay
@app.route('/relay/')
def relay():
	logs = Log.query.order_by(Log.logtime.desc()).all()
	return render_template('relay.html', logs=logs)

@app.route('/relay_on/<channel>')
def relay_on(channel):
	GPIO.setmode(GPIO.BCM)
	try:
		if(channel=='1'):
			GPIO.output(2, 1)
			db.session.add(Log("Channel#1, Pin#2 High"))
			db.session.commit()
			print("Channel 1 activated")
		elif(channel=='2'):
			GPIO.output(3, 1)
			db.session.add(Log("Channel#2, Pin#3 High"))
			db.session.commit()
			print("Channel 2 activated")
		print("ON Process complete. Good bye!")
	except KeyboardInterrupt:
		print("  Quit")
		GPIO.cleanup()
	logs = Log.query.order_by(Log.logtime.desc()).all()
	return render_template('relay.html', logs=logs)

@app.route('/relay_off/<channel>')
def relay_off(channel):
    GPIO.setmode(GPIO.BCM)
    try:
		if(channel=='1'):
			GPIO.output(2, 0)
			GPIO.output(3, 0)
			db.session.add(Log("Both Channel LOW"))
			db.session.commit()
			logs = Log.query.order_by(Log.logtime.desc()).all()
			return render_template('relay.html', logs=logs)
		elif(channel=='2'):
			GPIO.output(2, 0)
			GPIO.output(3, 0)
			db.session.add(Log("Both Channel LOW"))
			db.session.commit()
			logs = Log.query.order_by(Log.logtime.desc()).all()
			return render_template('relay.html', logs=logs)
		print("OFF Process complete. Good bye!")
    except KeyboardInterrupt:
        print("  Quit")
        # Reset GPIO settings
        GPIO.cleanup()
	logs = Log.query.order_by(Log.logtime.desc()).all()
	return render_template('relay.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

