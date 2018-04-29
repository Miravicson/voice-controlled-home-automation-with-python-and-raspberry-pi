"""The text recognize API uses the ibm watson_developer_cloud library associated with the python sdk for the
TextToSpeech transcription"""

import os

from watson_developer_cloud import TextToSpeechV1


class Transcribe:
    """This class encapsulates the IBM watson TextToSpeech API. this class is imported and the method output is called
    where ever text to speech transcription is needed.
    The method output saves an audio file 'output_en-US_LisaVoice.wav' as its output.
    the systems omxplayer is then used to play the audio file output. the output is not static and changes for each
    successful speech to text transcription"""
    # username = "186f4524-71ca-4fae-a75f-2e48971f8a9e" older password
    # password = "SouOx8v6VbWx"  older password
    # username = "5c965b52-48a2-42b2-98e5-c249511ad22b" old username
    # password = "K7Tfnlr21XeJ" old password
    username = "256a11df-05dc-41dd-b9ab-ea85f9200b1b"
    password = "WTMrCQ75hZIR"
    voice = "en-US_LisaVoice"
    # voice = "en-GB_KateVoice"
    # voice = "en-US_AllisonVoice"
    text_to_speech = TextToSpeechV1(username=username, password=password)
    base_dir = os.getcwd()
    base_dir2 = "/home/pi/Desktop/home_ai_annah"
    audio_commands = os.path.join(base_dir2, "audio_commands")

    fn = 'output_' + voice + '.wav'
    file_output = os.path.join(audio_commands, fn)

    def output(self, text):
        """Method takes text file as input and returns an audio file containing the voice transcription of the text
        it then calls the systems music player 'omxplayer' to play the transcribed audio corresponding to the
        text"""
        with open(self.file_output, 'wb') as audio_file:
            audio_file.write(self.text_to_speech.synthesize(text, voice=self.voice))

        os.system("omxplayer '{}'".format(self.file_output))
