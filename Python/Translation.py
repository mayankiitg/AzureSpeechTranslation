import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioConfig
import time

with open('/Users/mayankgupta/Projects/TTB/AzureCognitiveServices/key.txt', 'r') as f:
    speech_key = f.readline().rstrip()
service_region = "eastus"

# Creates an instance of a speech translation config with specified subscription key and service region.
# Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key, region=service_region)

# Sets source and target languages.
# Replace with the languages of your choice, from list found here: https://aka.ms/speech/sttt-languages
fromLanguage = 'en-US'
translation_config.speech_recognition_language = fromLanguage
translation_config.add_target_language('hi')

folderPath = '/Users/mayankgupta/Projects/TTB/AzureCognitiveServices/Results/'
fileName = 'speed_khan_academy' #'KhanAcademyLinearAlgebra' #'3blue1brown-channel-trailer'
fileExt = '.wav'
audio_config: AudioConfig = AudioConfig(filename=folderPath+fileName+fileExt)


def WriteToFile(results, fileName):
    with open(fileName, "wb") as f:
        for s in results:
            s += "\n"
            f.write(s.encode("UTF-8"))
            

def translate_microphone():

    # Creates a translation recognizer using and audio file as input.
    # By default it will use microphone.
    recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config)

    # Starts translation, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognized text as well as the translation.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    print("Say something...")
    result = recognizer.recognize_once()

    recognizer.start_continuous_recognition()

    # Check the result
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("RECOGNIZED '{}': {}".format(fromLanguage, result.text))
        print("TRANSLATED into {}: {}".format('fr', result.translations['hi']))
    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("RECOGNIZED: {} (text could not be translated)".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("NOMATCH: Speech could not be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("CANCELED: Reason={}".format(result.cancellation_details.reason))
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("CANCELED: ErrorDetails={}".format(result.cancellation_details.error_details))



def translate_continuous():
     # Creates a translation recognizer using and audio file as input.
    speech_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    all_results = []
    all_hindi_results = []
    def handle_final_result(evt):
        print('evt: {}'.format(evt.result.translations))
        all_results.append(evt.result.text)
        all_hindi_results.append(evt.result.translations['hi'])

    speech_recognizer.recognized.connect(handle_final_result)
    # Connect callbacks to the events fired by the speech recognizer
    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    # speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    # speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    # speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    # speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    print("Printing all results:")
    print(all_results)
    print(all_hindi_results)
    WriteToFile(all_results, f"Results/{fileName}_transcribe_eng.txt")
    WriteToFile(all_hindi_results, f"Results/{fileName}_translate_hindi.txt")

#translate_microphone()
translate_continuous()