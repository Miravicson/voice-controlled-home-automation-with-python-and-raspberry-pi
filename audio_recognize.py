# @Author :Ughonu Victor Chiagozie
# Date Created: February 15, 2017


import os
from os import system as speak
import json

import speech_recognition as sr
from watson_developer_cloud import SpeechToTextV1

"""This Class uses the speech recognition library to create an object
          that will listen to audio record and transcribe the recording """


class Listen:

    """This is the main class. it contains the method to listen to the microphone and return the welcome commands"""
    r = sr.Recognizer()
    m = sr.Microphone(sample_rate=16000)
    # IBM_USERNAME = "f1394c7e-9664-413b-8ece-2426138c6bdb" older username
    # IBM_USERNAME = "841498fa-7a18-4d49-9207-b75ac0a07357" old username
    # IBM_PASSWORD = "buMI6plnmhye" older password
    # IBM_PASSWORD = "PfFKHjaYAaib" old password
    IBM_USERNAME = "c13b3894-37b1-4a86-9225-a8636d9bc623"
    IBM_PASSWORD = "roLSkV3W1HYP"
    base_dir = os.getcwd()
    base_dir2 = "/home/pi/Desktop/home_ai_annah"
    audio_commands = os.path.join(base_dir2, 'audio_commands')


    ### create the object of the speech to text recognition interface of the python-sdk for ibm watson

    speech_to_text = SpeechToTextV1(
        username=IBM_USERNAME,
        password=IBM_PASSWORD,
        x_watson_learning_opt_out=True
    )

    # Main method begins, the return type is a string which could be the
    # transcribe audio or special errors

    def output(self):
        """This method calls the two other methods, introductions and listens"""
        # self.introductions()
        return self.listen()

    def unheard(self):
        """this method handles the audio feedback for unrecognized commands"""

        speak('omxplayer {0}'.format(os.path.join(self.audio_commands, 'unheard.ogg')))

    def introductions(self):

        """this method speaks the introduction commands for Annah"""
        speak('omxplayer {0}'.format(os.path.join(self.audio_commands, 'introductions3.ogg')))
        speak('omxplayer {0}'.format(os.path.join(self.audio_commands, 'request.ogg')))

    def listen(self):
        """This method listens for commands and adjust for audio source it returns the message corresponding to the
        voice input"""
        with self.m as source:
            self.r.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.r.listen(source)

        try:
            return self.r.recognize_ibm(audio, username=self.IBM_USERNAME,
                                        password=self.IBM_PASSWORD, show_all=False)
        except sr.UnknownValueError:
            return str(-1)
        except sr.RequestError:
            return str(404)

    def listen2(self):
        """This method of this class is used for testing the speech to text api when using the python-sdk interface
        for the Ibm watson developer cloud
        this method is used when imported into //stt_customizer.py// in the 'accessories' folder"""
        with self.m as source:
            self.r.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.r.listen(source)
            flac_data = audio.get_flac_data(
                convert_rate=None if audio.sample_rate >= 16000 else 16000,
                # audio samples should be at least 16 kHz
                convert_width=None if audio.sample_width >= 2 else 2  # audio samples should be at least 16-bit
            )

            try:
                print(json.dumps(self.speech_to_text.recognize(flac_data, content_type='audio/flac',
                                                               customization_id="3a2e04c0-5346-11e7-aeaf-57afcb850a3a",
                                                               model=None), indent=4))
            except sr.UnknownValueError:
                print(str(-1))
            except sr.RequestError:
                print(str(404))
