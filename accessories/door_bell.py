import RPi.GPIO as GPIO
import time
from os import system as speak

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
x = 0
while True:
    input_state = GPIO.input(21)
    x += 1
    print(x)
    if input_state == False:
        print("Button Pressed")
        print('>>>>>')
        time.sleep(0.2)
