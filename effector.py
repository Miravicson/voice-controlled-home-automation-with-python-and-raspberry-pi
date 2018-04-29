import os
import random
from datetime import datetime
import multiprocessing as mp
from os import system as speak  # The speak command is used to play static recorded audio files

import RPi.GPIO as GPIO  # Controls the pins on the raspberry pi
from models import Song, FoodTimetable, Weather  # The models contains details of static files
from text_recognize import Transcribe  # The Transcribe is a class of the text_recognize module. it contains a method
from audio_recognize import Listen

# which is an implementation of the watson developer cloud text to speech API

transcribe = Transcribe()  # The class that transcribes text into audio

audio_transcribe = transcribe.output  # A callback function derived from the method of
#  class Transcribe. It doest the transcription
base_dir = os.getcwd()
base_dir2 = "/home/pi/Desktop/home_ai_annah"
audio_commands = os.path.join(base_dir2, 'audio_commands')  # path to all the audio responses to commands

"""Turn on the light"""
sitting_room_light1 = room_1_light1 = 18
sitting_room_light2 = room_1_light2 = 19
sitting_room_light3 = room_1_light3 = 24
fan_pin = 25
olaoluwa_room = room_2_light = 23
jossy_room = room_3_light = 26
balcony_light = 8
door_bell_pin = 21


def enable_root():
    speak("sudo chown root.gpio /dev/gpiomem")
    speak("sudo chmod g+rw /dev/gpiomem")


def turn_on_light(audio_path=audio_commands, cb=audio_transcribe, room_number=None):
    enable_root()

    def on_light(led_pin):
        talk = cb
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_pin, GPIO.OUT)
        GPIO.setwarnings(False)
        GPIO.output(led_pin, True)

    if room_number == 1:
        on_light(room_1_light1)
        on_light(room_1_light2)
        on_light(room_1_light3)
        speak('omxplayer {0}'.format(os.path.join(audio_path, 'light_on.ogg')))

    if room_number == 2:
        on_light(room_2_light)
        speak('omxplayer {0}'.format(os.path.join(audio_path, 'light_on.ogg')))

    if room_number == 3:
        on_light(room_3_light)
        speak('omxplayer {0}'.format(os.path.join(audio_path, 'light_on.ogg')))


"""Turn off the light"""


def turn_off_light(audio_path=audio_commands, cb=audio_transcribe, room_number=None):
    enable_root()

    def off_light(led_pin):
        talk = cb
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_pin, GPIO.OUT)
        GPIO.setwarnings(False)
        GPIO.output(led_pin, False)

    if room_number == 1 or room_number is None:
        off_light(room_1_light1)
        off_light(room_1_light2)
        off_light(room_1_light3)
        speak('omxplayer {0}'.format(os.path.join(audio_path, 'light_off.ogg')))

    if room_number == 2:
        off_light(room_2_light)
        speak('omxplayer {0}'.format(os.path.join(audio_path, 'light_off.ogg')))

    if room_number == 3:
        off_light(room_3_light)
        speak('omxplayer {0}'.format(os.path.join(audio_path, 'light_off.ogg')))


"""Turn on the fan """


def turn_on_fan(audio_path=audio_commands, cb=audio_transcribe, room_number=None):
    enable_root()
    talk = cb
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fan_pin, GPIO.OUT)
    GPIO.setwarnings(False)
    GPIO.output(fan_pin, GPIO.HIGH)
    speak('omxplayer {0}'.format(os.path.join(audio_path, 'fan_on.ogg')))


"""Turn off the fan"""


def turn_off_fan(audio_path=audio_commands, cb=audio_transcribe, room_number=None):
    enable_root()
    talk = cb
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fan_pin, GPIO.OUT)
    GPIO.setwarnings(False)
    GPIO.output(fan_pin, GPIO.LOW)
    speak('omxplayer {0}'.format(os.path.join(audio_path, 'fan_off.ogg')))


"""Play song"""


def song_collection(audio_path=audio_commands, cb=audio_transcribe):
    talk = cb
    song = Song()
    song_list = song.list_song()
    print(song_list)
    songss = ', '.join(song_list)
    talk("Here are the songs available in your collection: " + songss)

    print(songss)


def sing_song(track=None, audio_path=audio_commands, num_play=0, cb=audio_transcribe):

    def play_song(default_path):
        os.system('omxplayer {0}'.format(default_path))

    talk = cb
    song = Song()
    all_song = song.song_list  # this is a list of all songs
    num_song = len(all_song)
    index_song = num_song - 1

    sample = random.randint(0,
                            index_song)  # this generates a random indexer to select a random song from the list
    sample = abs(sample - index_song)  # Further randomizes the song
    path2 = os.path.join(base_dir2, 'music')  # This gets the root folder containing the music
    default_path = os.path.join(path2,
                                all_song[sample])  # this indexes a random song from the list and creates a path to it
    song_name = song.song_name  # get the song's name from the instance of the Song class.

    speak('omxplayer {0}'.format(os.path.join(audio_commands, 'confirmation.ogg')))  # says "Sure just a second"

    try:
        song_path = os.path.join(path2, track)
        os.system('omxplayer {0}'.format(song_path))

    except Exception:
        default_song = os.path.basename(default_path)
        default_song = song_name[default_song]

        talk("I am about playing {0};".format(default_song))
        play_song(default_path=default_path)


"""Announce Food timetable"""


def announce_timetable(food_type, day_time=None, audio_path=audio_commands, cb=audio_transcribe):
    talk = cb
    timetable = FoodTimetable()
    food_timetable = timetable.food_timetable  # food_time table is a dictionary parsed from a json document
    my_date = datetime.now()
    day = '{0:%A}'.format(my_date).lower()
    format_time = '{0:%p}'.format(my_date).lower()

    if day_time is None:
        if format_time == "am":
            time = "morning"
            result = food_timetable[day][time]
            food_type = "breakfast"
            talk("The menu for {0} today is".format(food_type) + result)

        if format_time == "pm":
            time = "evening"
            result = food_timetable[day][time]
            food_type = "dinner"
            talk("The menu for {0} today is".format(food_type) + result)
    if day_time:
        time = day_time
        result = food_timetable[day][time]
        talk("The menu for {0} today is".format(food_type) + result)


"""Announce the time"""


def announce_date(audio_path=audio_commands, cb=audio_transcribe):
    talk = cb
    my_date = datetime.now()
    formatted_date = '{0:%A} {0:%B} {0:%d}, {0:%Y}.'.format(my_date)
    talk("Today is " + formatted_date)
    print(formatted_date)


def announce_time(audio_path=audio_commands, cb=audio_transcribe):
    talk = cb
    my_date = datetime.now()
    formatted_time = '{0:%I}:{0:%M} {0:%p}.'.format(my_date)
    talk("The time is " + formatted_time)


"""Announce weather"""


def announce_weather(audio_path=audio_commands, cb=audio_transcribe, day=None):
    talk = cb
    weather_object = Weather()
    weather = weather_object.weather

    def convert_temperature(temp_f=None, temp_c=None):
        if temp_c is None:
            temp_c = (5.0 / 9.0) * (temp_f - 32)
            return temp_c
        if temp_f is None:
            temp_f = (9.0 / 5.0) * temp_c + 32
            return temp_f

    """Remember to update the cron job to refresh the weather
     every 3 days so that these function will remain syntactically correct"""

    def actual_weather(i):
        whole_day = weather["forecasts"][i]
        day_forecast = weather["forecasts"][i]["day"]
        night_forecast = weather["forecasts"][i]["night"]
        max_temp_c = convert_temperature(temp_f=whole_day["max_temp"])
        min_temp_c = convert_temperature(temp_f=whole_day["min_temp"])
        day_shortcast = day_forecast["shortcast"]
        night_shortcast = night_forecast["shortcast"]
        day_temp = convert_temperature(temp_f=day_forecast["temp"])
        night_temp = convert_temperature(temp_f=night_forecast["temp"])
        day_relative_humidity = day_forecast["rh"]
        night_relative_humidity = day_forecast["rh"]
        # day_rain = night_forecast["precip_type"]
        # night_rain = night_forecast["precip_type"]
        # narrative = whole_day["narrative"]

        start_forecast = "This is the weather report for Lagos. Today's temperature range is from {0:0.1f} degree centigrade" \
                         ", at the lowest, and {1:0.1f} degree centigrade, at maximum. Average daily temperature is " \
                         "{6:0.1f} degree centigrade and the average nightly temperature is {7:0.1f} degree centigrade." \
                         " During the day the relative humidity is {2:0.1f} percent and at night " \
                         "the relative humidity is {3:0.1f} percent. It is going to be {4} during the day " \
                         "and {5}, at night."

        inter_forecast = start_forecast.format(min_temp_c,
                                               max_temp_c,
                                               day_relative_humidity,
                                               night_relative_humidity,
                                               day_shortcast,
                                               night_shortcast,
                                               day_temp,
                                               night_temp)
        return inter_forecast

    if day == "today" or day is None:
        talk(actual_weather(0))

    if day is not None and day.lower() == "tomorrow":
        talk(actual_weather(1))


"""Tell me about yourself"""


def read_story(audio_path=audio_commands, cb=audio_transcribe):
    talk = cb
    file_location = "/home/pi/Desktop/home_ai_annah/about_annah.txt"
    with open(file_location, "r") as f:
        about = f.read()
        talk(about)


"""Switch over to generator"""


def generator(audio_path=audio_commands, cb=audio_transcribe):
    enable_root()
    talk = cb
    talk("The generator has been switched on")


def sim_module():
    print("I control the circuit from sms")
    pass


def reply_greeting(audio_path=audio_commands, cb=audio_transcribe, message=None):
    talk = cb
    # enable_root()
    my_date = datetime.now()
    formatted_time = '{0:%I}:{0:%M} {0:%p}.'.format(my_date)
    if "AM" in formatted_time:
        if "good morning" in message:
            talk("Good morning to you, how are you?")
        else:
            talk("It's morning, good morning to you. How are you?")
        # talk("The time is {0}. {1}" + formatted_time)
    elif "PM" in formatted_time and (int(formatted_time[0:2]) < 6 or int(formatted_time[0:2]) == 12):
        if "good afternoon" in message:
            talk("Good afternoon to you,how are you?")
        else:
            talk("It's afternoon, good afternoon to you. How are you?")
    elif "PM" in formatted_time and int(formatted_time[0:2]) >= 6:
        if "good evening" in message:
            talk("Wishing you a lovely evening, I am fine, how are you?")
        else:
            talk("It's evening, good evening. How are you?")
