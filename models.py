import json
import os

"""This module contains all static information like the food timetable and list of songs"""


class Song:
    base_dir2 = "/home/pi/Desktop/home_ai_annah"  # Note: this path is hardcoded so that it can be ran by the crontab
    # at runtime

    def __init__(self):
        self.song_list = os.listdir(os.path.join(self.base_dir2, 'music'))
        # This dictionary maps the files stored in the music directory to its name so Annah can recognize the songs
        # the songs are stored using the next cardinal digit with the extension ".mp3" eg. 1.mp3
        # It is important to remember to update this dictionary when you add a song to the music folder

        self.song_name = {
            # '2.mp3': 'Remember me.',
            # '1.mp3': 'The moment I knew.',
            # '3.mp3': 'The months of Sundays.',
            # '4.mp3': 'Smile for me',
            # '5.mp3': 'A prayer for a friend.',
            # '6.mp3': 'This God is too good.',
            # '7.mp3': 'Riding to New York.',
            # '8.mp3': 'Things you have never done.',
            # '9.mp3': 'Chemistry.',
            '2.mp3': '"Everything has changed". by; Taylor Swift and Ed Sheeran.',
            '1.mp3': '"Everything has changed". by; Taylor Swift and Ed Sheeran.',
            '3.mp3': '"Everything has changed". by; Taylor Swift and Ed Sheeran.',
            '4.mp3': '"Everything has changed". by; Taylor Swift and Ed Sheeran.',
            '5.mp3': '"Everything has changed". by; Taylor Swift and Ed Sheeran.',
            '6.mp3': '"Everything has changed". by; Taylor Swift and Ed Sheeran.',
            '7.mp3': '"Everything has changed". by; Taylor Swift and Ed Sheeran.',
            '8.mp3': '"Everything has changed". by; Taylor Swift and Ed Sheeran',
            '9.mp3': '"Everything has changed". by; Taylor Swift and Ed Sheeran.'

        }

    def list_song(self):
        """This method of the class Song iterates through all the songs contained in the song_name dictionary
        and returns a list of strings of song names"""
        song_names = []
        for song in self.song_name:
            song_names.append(self.song_name[song])
        return song_names


class FoodTimetable:
    """This class loads the JSON file for the food timetable. It returns a dictionary containing keys
    that contain an inner key of 'morning' and 'evening'. Each of the inner keys then has a value of
     the respective food for the periods of morning and evening respectively."""

    food_path = "/home/pi/Desktop/home_ai_annah/food_timetable.json"  # The path is hardcoded so that it can be ran with

    #  the crontab at startup

    @staticmethod
    def get_json():
        """This method loads the json file 'food_timetable.json' and returns a json object. It is
        called in the __init__ method."""

        with open(FoodTimetable.food_path, 'r') as food_file:
            food_file = food_file.read()
            food_timetable = json.loads(food_file)
            return food_timetable

    def __init__(self):
        """This method initialises the class by setting a class variable of food_timetable
        to the return value of the static method get_json."""

        self.food_timetable = self.get_json()


class Weather:
    """This class loads the JSON file for the weather_data.json. It returns a dictionary
    containing weather reports."""
    weather_path = "/home/pi/Desktop/home_ai_annah/weather_data.json"

    @staticmethod
    def get_json():
        """This method loads the json file 'weather_data.json' and returns a json object.
         It is called in the __init__ method."""

        with open(Weather.weather_path, 'r') as weather_data:
            weather_temp = weather_data.read()
            weather = json.loads(weather_temp)
            return weather

    def __init__(self):
        """This method initialises the class by setting a class variable of weather
        to the return value of the static method get_json."""

        self.weather = self.get_json()
