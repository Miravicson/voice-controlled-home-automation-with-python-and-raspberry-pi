import RPi.GPIO as GPIO                    #Import GPIO library

#The method that would call this class will scan both nepa input and
#generator input. it will also switchover base on priority nepa is top priority.
class changeoverswitch:
    GPIO.setmode(GPIO.BCM)

    generator = 20
    nepa = 21
    generatorsource = 27
    nepasource = 28

    def __init__(self):

        #pin setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.generator,GPIO.OUT)
        GPIO.setup(self.nepa,GPIO.OUT)

    def switchover(self,powersource):
        if powersource == "generator":
            GPIO.output(self.generator, GPIO.HIGH)
            GPIO.output(self.nepa, GPIO.LOW)
        elif powersource == "nepa":
            GPIO.output(self.nepa, GPIO.HIGH)
            GPIO.output(self.generator, GPIO.LOW)
        elif powersource == "offall":
            GPIO.output(self.nepa, GPIO.LOW)
            GPIO.output(self.generator, GPIO.LOW)
