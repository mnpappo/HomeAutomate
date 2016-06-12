import Adafruit_DHT
from flask import Flask, flash, render_template, request, abort, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# db configs
app.config.from_pyfile('db.cfg')
db = SQLAlchemy(app)

#import models
from models import *

# pin setups
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# set pin numbers
led = 18
gas = 23
relay_ch1 = 5
relay_ch2 = 6
humTemp = 4
ldr = 24
pinList = [relay_ch1, relay_ch2, led]
for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.LOW)


###--API--###
@app.route('/api/', methods=['GET'])
def api_home():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, humTemp)

    data = [
        {
            'mgs': 'Welcome Mr.X',
	    'humidity': humidity,
	    'temperature': temperature
	}
    ]


    return jsonify({'data': data})
    

@app.route('/api/led_on', methods=['GET'])
def api_led_on():
    GPIO.setup(led, GPIO.IN)
    state = GPIO.input(led)
    mgs = 'on'
    if state:
        print("LED is already ON state!")
        GPIO.setup(led, GPIO.OUT)
        mgs = 'already_on'
    else:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, 1)
        print("LED ON")
        mgs = 'success'


    data = [
	{
	    'mgs': mgs
	}	   
    ]
    
    return jsonify({'data': data})


@app.route('/api/led_off', methods=['GET'])
def api_led_off():
    GPIO.setup(led, GPIO.IN)
    state = GPIO.input(led)
    mgs = 'off'
    if state:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, 0)
        print("LED OFF")
        mgs = 'success'
    else:
        print("LED is already OFF state!")
        mgs = 'already_off'


    data = [
        {
            'mgs': mgs
        }          
    ]   

    return jsonify({'data': data})


@app.route('/api/gas_detect/')
def api_gas_detect():
    GPIO.setup(gas, GPIO.IN)
    val = GPIO.input(gas)
    
    data = [
	{
	    'mgs': val
	}
    ]

    return jsonify({'data': data})


#@app.route('/api/')


######--Controllers---########
@app.route('/')
def home():
    return render_template('home.html')

#login+registration
@app.route('/login/')
def login():
    return render_template('login.html')

# led

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
        GPIO.output(led, 1)
        print("LED ON")
        return render_template('home.html')
    return render_template('home.html')


@app.route('/led_off/')
def led_off():
    GPIO.setup(led, GPIO.IN)
    state = GPIO.input(led)
    if state:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, 0)
        print("LED OFF")
        return render_template('home.html')
    else:
        print("LED is already OFF state!")
        return render_template('home.html')
    return render_template('home.html')

# humidity & temperature

@app.route('/getHumTemp/')
def getHumTemp():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, humTemp)
    return render_template('humTemp.html', hum = humidity, temp = temperature)

# GAS
@app.route('/gasDetect/')
def gasDetect():
    GPIO.setup(gas, GPIO.IN)
    val = GPIO.input(gas)
    print(type(val))
    print(val)
    return render_template('gas.html', gas = val)

# LDR

def RCtime(RCpin):
        reading = 0
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(RCpin, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
        while (GPIO.input(RCpin) == GPIO.LOW):
                reading += 1
        return reading

@app.route('/ldr/')
def getLdr():
    ldr_value = RCtime(ldr)
    print(ldr_value)
    return render_template('ldr.html', ldr_value = ldr_value) 
# relay

@app.route('/relay/')
def relay():
    logs = Log.query.order_by(Log.logtime.desc()).all()
    return render_template('relay.html', logs=logs)


@app.route('/relay_on/<channel>')
def relay_on(channel):
    GPIO.setmode(GPIO.BCM)
    try:
        if(channel == '1'):
            GPIO.output(relay_ch1, 1)
            db.session.add(Log("Channel#1, Pin#5 High"))
            db.session.commit()
            print("Channel 1 activated")
        elif(channel == '2'):
            GPIO.output(relay_ch2, 1)
            db.session.add(Log("Channel#2, Pin#6 High"))
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
        if(channel == '1'):
            GPIO.output(relay_ch1, 0)
            GPIO.output(relay_ch2, 0)
            db.session.add(Log("Both Channel LOW"))
            db.session.commit()
            logs = Log.query.order_by(Log.logtime.desc()).all()
            return render_template('relay.html', logs=logs)
        elif(channel == '2'):
            GPIO.output(relay_ch1, 0)
            GPIO.output(relay_ch2, 0)
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
