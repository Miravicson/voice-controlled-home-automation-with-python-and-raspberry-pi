import speech_recognition as sr
import os
class Listen:

    """This is the main class. it contains the method to listen to the microphone and return the welcome commands"""
    r = sr.Recognizer()
    m = sr.Microphone(sample_rate=16000)
    IBM_USERNAME = "f1394c7e-9664-413b-8ece-2426138c6bdb"
    IBM_PASSWORD = "buMI6plnmhye"
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
        self.introductions()
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


def callback(recogn)