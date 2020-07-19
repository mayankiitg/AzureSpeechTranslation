import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioConfig
import time
from Utils import readSpeechKey, getServiceRegion

########### CONFIGURTATION #####
STORE_TO_FILE = 1
folderPath = '../Results/'
fileName = 'speed_khan_academy_translate_hindi.txt' #'KhanAcademyLinearAlgebra' #'3blue1brown-channel-trailer'
audio_filename = "../Results/sample_audio.wav"
#########

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key = readSpeechKey()
service_region = getServiceRegion()

def create_speech_config():
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_language = 'hi-IN'
    speech_config.speech_recognition_language = 'hi-IN'
    return speech_config

def create_audio_output_config():
# Creates an audio configuration that points to an audio file.
    audio_output = speechsdk.audio.AudioOutputConfig(filename=audio_filename)
    return audio_output

def text_to_speech():
    speech_config = create_speech_config()
    audio_output_config = create_audio_output_config()

    if STORE_TO_FILE:
        # Creates a synthesizer with the given settings
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output_config)
    else:
        # Creates a speech synthesizer using the default speaker as audio output.
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    with open(folderPath+fileName, "r", encoding='utf8') as f:
        text = f.read()

    print(text)

    # Synthesizes the received text to speech.
    # The synthesized speech is expected to be heard on the speaker with this line executed.
    result = speech_synthesizer.speak_text_async(text).get()

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        if STORE_TO_FILE:
            print("Speech synthesized to [{}] for text [{}]".format(audio_filename, text))
        else:
            print("Speech synthesized to speaker for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")

text_to_speech()