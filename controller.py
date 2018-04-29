"""The controller module contains code to filter the input commands and call related effector functions.
    It filters the input commands using simple if statements as well as regular expressions.
    The controller uses the Listen class from the voice_capture file
"""

import re
import RPi.GPIO as GPIO
from text_recognize import Transcribe  # This class handles text to speech transcription
from audio_recognize import Listen  # This class handles speech to text transcription
import effector  # This module contains most methods for handling instructions
import os
import multiprocessing as mp
import time

from datetime import datetime

from os import system as speak

""" Here we import the module for text to speech translation."""
transcribe = Transcribe()
talk = transcribe.output  # we created a call back but did not call the function\

#######################################################################################################

""" Here we instantiate the speech to text  class"""
listener = Listen()
listener.introductions()  # The introduction functions speaks Annah's name and prompts the user to give instructions

#######################################################################################################

""" Here we encode the absolute path to the parent directory. This is important when using crontab jobs"""

base_dir2 = "/home/pi/Desktop/home_ai_annah"  # Note: this path is hardcoded so that it can be ran by the crontab
audio_path = os.path.join(base_dir2, "audio_commands")

#######################################################################################################

""" Here we define the call_effector function. This function takes in speech to text generated message and calls 
the relevant effector method"""


def call_effector(message, global_variable=0):
    """Switch on The light"""

    light_pattern = r'lights?|bulbs?|[^n\s]+ights?|\w+ite'  # Regular expression pattern to match light
    switch_pattern_on = r'\bon\b'  # Regular expression pattern to match on
    switch_pattern_off = r'\boff?\b'
    if re.search(light_pattern, message) and re.search(switch_pattern_on, message) and global_variable == 0:
        if "room one " in message:
            effector.turn_on_light(room_number=1)
            global_variable += 1
        if "room two" in message:
            effector.turn_on_light(room_number=2)
            global_variable += 1
        if "room three" in message:
            effector.turn_on_light(room_number=3)
    if re.search(light_pattern, message) and re.search(switch_pattern_off, message) and global_variable == 0:
        if "room one" in message:
            effector.turn_off_light(room_number=1)
            global_variable += 1
        if "room two" in message:
            effector.turn_off_light(room_number=2)
            global_variable += 1
        if "room three" in message:
            effector.turn_off_light(room_number=3)
            global_variable += 1

    """ Reply to greeting """

    if "good morning" in message or "good afternoon" in message or "good evening" in message and global_variable == 0:
        effector.reply_greeting(message=message)
        global_variable += 1

    """Switch on the fan"""

    fan_pattern = r'the(ier)?\sf\w*\b|the(ier)?\sphone'
    if re.search(fan_pattern, message) and re.search(switch_pattern_on, message) and global_variable == 0:
        effector.turn_on_fan()
        global_variable += 1
    if re.search(fan_pattern, message) and re.search(switch_pattern_off, message) and global_variable == 0:
        effector.turn_off_fan()
        global_variable += 1

    """Play Song"""
    song_pattern = r'sungs?|songs?|musics?|sunks?'
    play_pattern = r'play|way|sings?(ing)?|start'
    next_pattern = r'another|next|\wext'
    collection_pattern = r'collections?'

    if re.search(song_pattern, message) and global_variable == 0:
        if re.search(play_pattern, message):
            effector.sing_song()
            global_variable += 1
        # if re.search(next_pattern, message):
        #     effector.next_song()
        #     global_variable += 1
        if re.search(collection_pattern, message):
            effector.song_collection()
            global_variable += 1

    """Food Timetable"""
    morning_pattern = 'morning|breakfast|break\sfast'
    afternoon_pattern = 'afternoon'
    evening_pattern = 'evening|dinner|night'

    food_pattern = 'foods?|\seats?(ing)?\s|breakfast|break\sfast|evening|dinner|\bnight\b'

    if re.search(food_pattern, message) and global_variable == 0:

        if re.search(morning_pattern, message):
            effector.announce_timetable(food_type="breakfast", day_time="morning")
            global_variable += 1
        elif re.search(evening_pattern, message):
            effector.announce_timetable(food_type="dinner", day_time="evening")
            global_variable += 1
        else:
            effector.announce_timetable(food_type=None)
            global_variable += 1

    """Announce the time"""

    time_pattern = r'time|type|\btie\b'

    if re.search(time_pattern, message) and global_variable == 0:
        effector.announce_time()
        global_variable += 1

    """Announce Date"""
    date_pattern = r'dates?| \w+ates?'

    if re.search(date_pattern, message) and global_variable == 0:
        effector.announce_date()
        global_variable += 1

    """About Anna"""

    about_pattern = r'story|yourself|about'

    if re.search(about_pattern, message):
        effector.read_story()
        global_variable += 1

    """Announce weather"""

    weather_pattern = r'whether|weather'

    if re.search(weather_pattern, message) and global_variable == 0:
        if "today" in message:
            day = "today"
        elif "tomorrow" in message:
            day = "tomorrow"
        else:
            day = None
        effector.announce_weather(day=day)
        global_variable += 1

    if global_variable < 1:
        return 1


#####################################################################################################

""" Here we handle the ultrasonic sensor detection"""


def ultrasonic(trig, echo, conn, name):
    os.system("sudo chown root.gpio /dev/gpiomem")  # gives the ultrasonic sensor root access to the gpio
    os.system("sudo chmod g+rw /dev/gpiomem")  # gives the ultrasonic sensor root access to the gpio

    GPIO.setmode(GPIO.BCM)  # sets the gpio board to broadcom numbering system

    GPIO.setup(trig, GPIO.OUT)  # sets the trigger pin as a gpio output pin
    GPIO.setup(echo, GPIO.IN)  # sets the echo pin as a gpio input pin

    while True:  # keeps listening for signals forever
        GPIO.output(trig, False)  # Set the trig1 to low
        time.sleep(1)  # Delay the sensor until it gets ready

        GPIO.output(trig, True)  # Starts a pulse

        time.sleep(0.00001)  # waits for 10 micro-seconds

        GPIO.output(trig, False)  # stops the pulse

        pulse_start1 = 0  # initial value for pulse start time
        pulse_end1 = 0  # initial value for pulse end time

        while GPIO.input(echo) == 0:  # checks to see if the echo pin sees a low
            pulse_start1 = time.time()  # measures the time when echo sees a low and initializes the pulse start time

        while GPIO.input(echo) == 1:  # checks to see if the echo pin sees a high
            pulse_end1 = time.time()  # keeps recording the time as long as echo is high and stores the value to the pulse_end

        pulse_duration1 = pulse_end1 - pulse_start1  # calculates the pulse width

        distance = pulse_duration1 * 17150  # multiplies by the speed of sound, in cm/s, divided by 2

        distance = round(distance, 2)  # rounds up the distance to 2 decimal places

        if 2 < distance < 400:  # ensures the ultrasonic sensor is within valid ranges, 2 cm and 400 cm
            conn.send([name, distance])  # sends this distance to the parent process via a PIPE

        else:
            conn.send([name, ""])  # if the distance is not within range it sends "Out of Range"


#####################################################################################################
""" Here we write instructions to handle the press of  the door bell"""


def door_bell():
    os.system("sudo chown root.gpio /dev/gpiomem")
    os.system("sudo chmod g+rw /dev/gpiomem")
    GPIO.setmode(GPIO.BCM)
    door_bell_pin = 21
    GPIO.setup(door_bell_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #

    while True:
        input_state = GPIO.input(door_bell_pin)
        if input_state == 0:  # Listen for the first press
            while input_state == 0:
                input_state = GPIO.input(door_bell_pin)
            time.sleep(2)  # Wait for two seconds
            input_state = GPIO.input(door_bell_pin)
            if input_state == 0:  # if the bell is pushed for more than 2 seconds
                speak("omxplayer {0}".format(os.path.join(audio_path, 'afriend.ogg')))  # say someone we know is at door
                while input_state == GPIO.input(door_bell_pin):
                    input_state = GPIO.input(door_bell_pin)
            else:
                speak("omxplayer {0}".format(os.path.join(audio_path, "stranger.ogg")))  # say a stranger is at the door


########################################################################################################
""" Instructions to turn on the balcony light at night (7:00 pm) and turn it off in the morning (6:00 am) """


def light_timer():
    """This function controls the light in the balcony"""

    os.system("sudo chown root.gpio /dev/gpiomem")  # grants the light_timer root access to the gpio
    os.system("sudo chmod g+rw /dev/gpiomem")  # grants the light_timer root access to the gpio
    while True:  # This code runs forever
        formatted_time = '{0:%H}{0:%M}'.format(datetime.now())  # gets the current time and formats it in a 24 hr format
        numeric_time = int(formatted_time)  # converts the formated time to an integer
        if (0 <= numeric_time <= 600) or (
                        1900 <= numeric_time <= 2359):  # if the time is between 7pm and 11:59pm and also between 12am and 6am the light should be on
            GPIO.setmode(GPIO.BCM)  # sets the gpio mode as broadcom
            GPIO.setup(8, GPIO.OUT)  # sets the gpio pin 8 as the balcony_light pin
            GPIO.setwarnings(False)  # disables gpio warnings
            GPIO.output(8, True)  # turns on the light
        else:  # At any other time outside the range of 7pm to 6am, the light will be turned off
            GPIO.setmode(GPIO.BCM)  # set the gpio mode as broadcom
            GPIO.setup(8, GPIO.OUT)  # sets the gpio pin 8 as the balcony_light pin
            GPIO.setwarnings(False)  # disables the gpio warnings
            GPIO.output(8, False)  # turns off the light


#########################################################################################################

def listener_function(conn):
    listener_2 = Listen()
    while True:
        message_2 = listener_2.output()
        conn.send(message_2)
        time.sleep(0.8)


""" we define the processes to run and the pipes for communication with the parent process here."""
ultra1_par, ultra1_child = mp.Pipe()  # creates pipe for the first ultrasonic sensor process and parent process
ultra2_par, ultra2_child = mp.Pipe()  # creates pipe for the second ultrasoinic sensor process and the parent process
door_bell_par, door_bell_child = mp.Pipe()  # creates pipe for the door bell and the parent process
light_timer_par, light_timer_child = mp.Pipe()  # creates pipe for the light timer process and the parent process
listener_par, listener_child = mp.Pipe()  # creates pipe for the listener and the parent process

ultra1 = mp.Process(target=ultrasonic, args=(20, 16, ultra1_child, "ultrasonic1"))
ultra2 = mp.Process(target=ultrasonic, args=(17, 22, ultra2_child, "ultrasonic2"))
doorbell_process = mp.Process(target=door_bell)
lighttimer_process = mp.Process(target=light_timer)
listener_process = mp.Process(target=listener_function, args=(listener_child,))

ultra1.start()
ultra2.start()
doorbell_process.start()
lighttimer_process.start()
listener_process.start()
number_of_people = 0
ultrasonic_distance_range = 200

#########################################################################################################
#########################################################################################################

""" The looping starts here. This loop contains set of instructions that are to run forever"""

while True:

    distance1 = ultra1_par.recv()           # Gets distance1 from ultrasonic sensor 1 child process "ultra1"

    distance2 = ultra2_par.recv()           # Gets distance2 from ultrasonic sensor 2 child process "ultra2"

    # print("{0[0]} : {0[1]}".format(distance1, distance2))
    distance1 = distance1[1]
    distance2 = distance2[1]

    if isinstance(distance1, int) and distance1 < ultrasonic_distance_range:
        if isinstance(distance2, int) and distance2 < ultrasonic_distance_range:
            number_of_people += 1
        else:
            print("nobody detected going in")

    elif isinstance(distance2, int) and distance2 < ultrasonic_distance_range:
        if isinstance(distance1, int) and distance1 < ultrasonic_distance_range:
            number_of_people -= 1
        else:
            print("nobody detected going out")

    message = listener_par.recv()               # Receives transcribe audio from listener class.
    print(message)
    if "Annah" in message or "Anna" in message:  # This line ensures that Annah only responds to commands when it hears it's name
        def handle_effector(message):
            return_value = call_effector(message)  # calls the effector function with the transcribed audio text
            if return_value:
                listener.unheard()
                message = listener_par.recv()
                print(message)
                handle_effector(message)


        handle_effector(message)

        speak('omxplayer {0}'.format(
            os.path.join(audio_path, 'next_command.ogg')))  # Says I am waiting for your next command
        print("I am waiting for your next command")
