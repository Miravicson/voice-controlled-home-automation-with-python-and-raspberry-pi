import os
import RPi.GPIO as GPIO

led_pin = 23

def enable_root():

	os.system("sudo chown root.gpio /dev/gpiomem")
	os.system("sudo chmod g+rw /dev/gpiomem")


def turn_on_light(led_pin):
	enable_root()

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(led_pin, GPIO.OUT)
	GPIO.setwarnings(False)
	GPIO.output(led_pin, True)
	print("I have turned on the light")
	# GPIO.cleanup()

def turn_off_light(led_pin):
	enable_root()

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(led_pin, GPIO.OUT)
	GPIO.setwarnings(False)
	GPIO.output(led_pin, GPIO.LOW)
	print("I have turned off the light")
	# GPIO.cleanup()


