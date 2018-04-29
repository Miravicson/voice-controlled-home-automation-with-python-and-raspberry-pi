# Code to scan for nepa and generator
import RPi.GPIO as GPIO  # Import GPIO library

from accessories.changeover import changeoverswitch


# The method that would call this class will scan both nepa input and
# generator input. it will also switchover base on priority nepa is top priority.
class changeoverscanner:
    GPIO.setmode(GPIO.BCM)

    generatorsource = 27
    nepasource = 28
    nepastatus = "off"
    geneeratorstatus = "off"

    def __init__(self):

        # pin setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.generatorsource, GPIO.IN)
        GPIO.setup(self.nepasource, GPIO.IN)

    def scanpowersource(self):
        nepa = "nepa"
        generator = "generator"
        while GPIO.input(self.generatorsource) == 1:
            print("There is power in Generator")
            if GPIO.input(self.nepasource) == 1:
                print("There is power in nepa")
                # Since nepa has a higher priority than generator, in would sound
                # an alarm and automatically switch to nepa
                # countdown 5secs
                # switchover to nepa
                if self.nepastatus == "off":
                    switch = changeoverswitch()
                    switch.switchover(nepa)
                    self.nepastatus = "on"
            else:
                if self.generatorstatus == "off":
                    switch = changeoverswitch()
                    switch.switchover(generator)
                    self.generatorstatus = "on"

        # while not GPIO.input(self.nepasource) == 0:
        #     print("There is light")
        #     if self.nepastatus == "off":
        #         switch = changeoverswitch()
        #         switch.switchover(nepa)
        #         self.nepastatus = "on"
        #
        #     if GPIO.input(self.generatorsource):
        #         print("There is power in Generator")
        #         # But because of nepa has a higher priotity than generator.
        #         # We wont be switching over.
