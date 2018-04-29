"""this script is used to perform operations on the the speech to text api. the operations are such as
(1) adding a custom model....
    this is done using the listener.speech_to_text.create_custom_models().
(2) list the custom models created for the speech to text service.
(3) delete and update models and corpora.



I used three interfaces to access the Ibm speech to text API. The interfaces are

(1)The python-sdk ibm developer cloud.
(2)The python speech to text library. I did some serious work under the hood.
(3)The curl interface using ssh commands

"""

from audio_recognize import Listen

listener = Listen()
print("Say Something")
listener.listen2()









# print("Listing custom models")
#
# result2 = listener.speech_to_text.list_custom_models()
# print(result2)
#
#
# print("Listing corpora")
#
# result3 = listener.speech_to_text.list_corpora(customization_id="5c081c90-29be-11e7-a25c-3515edf602ac")
#
# print(result3)