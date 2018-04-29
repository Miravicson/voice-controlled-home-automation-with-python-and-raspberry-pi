import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import time library


class ultrasonicsensordetector:
    TRIG1 = 23  # Associate pin 23 to TRIG
    ECHO1 = 24  # Associate pin 24 to ECHO

    TRIG2 = 25  # Associate pin 23 to TRIG
    ECHO2 = 26  # Associate pin 24 to ECHO
    noofpeople = 0  # No of people in the room

    def __init__(self):

        GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering
        GPIO.setup(self.TRIG1, GPIO.OUT)  # Set pin as GPIO out
        GPIO.setup(self.ECHO1, GPIO.IN)  # Set pin as GPIO in

        GPIO.setup(self.TRIG2, GPIO.OUT)  # Set pin as GPIO out
        GPIO.setup(self.ECHO2, GPIO.IN)  # Set pin as GPIO in

    def detectmovement(self):
        print("Movement direction in progress")

        while True:

            GPIO.output(self.TRIG1, False)  # Set TRIG1 as LOW
            GPIO.output(self.TRIG2, False)  # Set TRIG2 as LOW
            print("Waitng For Sensor To Settle")
            time.sleep(2)  # Delay of 2 seconds

            GPIO.output(self.TRIG1, True)  # Set TRIG1 as HIGH
            GPIO.output(self.TRIG2, True)  # Set TRIG2 as HIGH
            time.sleep(0.00001)  # Delay of 0.00001 seconds
            GPIO.output(self.TRIG1, False)  # Set TRIG1 as LOW
            GPIO.output(self.TRIG2, False)  # Set TRIG2 as LOW

            while GPIO.input(self.ECHO1) == 0:  # Check whether the ECHO1 is LOW

                while GPIO.input(self.ECHO2) == 0:  # Check whether the ECHO2 is LOW

                    # To check the direction of movement
                    # Foward movement means ECHO1 then ECHO2
                    while GPIO.input(self.ECHO1) == 1:  # Check whether the ECHO1 is HIGH
                        if GPIO.input(self.ECHO2) == 1:  # Check whether the ECHO2 is HIGH
                            # movement = "Forward: Out of the room" #Reduce the number of people in the room
                            self.noofpeople -= 1
                            # else: movement = "No Movement"

                            # Backward movement means ECHO2 then ECHO1.
                    while GPIO.input(self.ECHO2) == 1:  # Check whether the ECHO2 is HIGH
                        if GPIO.input(self.ECHO1) == 1:  # Check whether the ECHO1 is HIGH
                            movement = "Backward: Into the room"
                            self.noofpeople += 1  # Increase the number of people in the room

        return self.noofpeople;  # When the number of people in a room goes to zero
        # Automatically turn off the light in that room
        # These code as to be in a thread.
