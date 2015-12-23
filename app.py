from flask import Flask, render_template
from gpiozero import LED
import RPi.GPIO as GPIO
import time

led1 = LED(4)
# init list with pin numbers
pinList = [2, 3]
# time to sleep between operations in the main loop
SleepTimeL = 2
# loop through pins and set mode and state to 'low'
for i in pinList:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.LOW)

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

#led
@app.route('/led_on/')
def led_on():
	led1.on()
	return render_template('home.html')

@app.route('/led_off/')
def led_off():
	led1.off()
	return render_template('home.html')

#relay
@app.route('/relay/')
def relay():
	return render_template('relay.html')

@app.route('/relay_on/<channel>')
def relay_on(channel):
	GPIO.setmode(GPIO.BCM)
	try:
		if(channel=='1'):
			GPIO.output(2, GPIO.HIGH)
			print("Channel 1 activated")
			time.sleep(SleepTimeL)
			#pinList.reverse()
		elif(channel=='2'):
			GPIO.output(3, GPIO.HIGH)
			print("Channel 2 activated")
			time.sleep(SleepTimeL)
			#pinList.reverse()
		print("ON Process complete. Good bye!")
		#pinList.reverse()
	except KeyboardInterrupt:
		print("  Quit")
		GPIO.cleanup()
	return render_template('relay.html')

@app.route('/relay_off/<channel>')
def relay_off(channel):
    GPIO.setmode(GPIO.BCM)
    try:
		if(channel=='1'):
			GPIO.output(2, GPIO.LOW)
			print("Channel 1 deactivated")
			time.sleep(SleepTimeL)
			#pinList.reverse()
			return render_template('relay.html')
		elif(channel=='2'):
			GPIO.output(3, GPIO.LOW)
			print("Channel 2 deactivated")
			time.sleep(SleepTimeL)
			#pinList.reverse()
			return render_template('relay.html')
		print("OFF Process complete. Good bye!")
    except KeyboardInterrupt:
        print("  Quit")
        # Reset GPIO settings
        GPIO.cleanup()
	return render_template('relay.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

