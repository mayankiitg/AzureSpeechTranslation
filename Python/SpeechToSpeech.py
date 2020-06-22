import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.translation import TranslationSynthesisResult

########### CONFIGURTATION #####
STORE_TO_FILE = 1
folderPath = '/Users/mayankgupta/Projects/TTB/AzureCognitiveServices/Results/'
fileName = 'KhanAcademyLinearAlgebratranslate_hindi.txt' #'KhanAcademyLinearAlgebra' #'3blue1brown-channel-trailer'

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
with open('/Users/mayankgupta/Projects/TTB/AzureCognitiveServices/key.txt', 'r') as f:
    speech_key = f.readline().rstrip()
service_region = "eastus"
#########

def translate_speech_to_speech():

    # Creates an instance of a speech translation config with specified subscription key and service region.
    # Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
    translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key, region=service_region)

    # Sets source and target languages.
    # Replace with the languages of your choice, from list found here: https://aka.ms/speech/sttt-languages
    fromLanguage = 'en-US'
    toLanguage = 'hi-IN'
    translation_config.speech_recognition_language = fromLanguage
    translation_config.add_target_language(toLanguage)

    # Sets the synthesis output voice name.
    # Replace with the languages of your choice, from list found here: https://aka.ms/speech/tts-languages
    translation_config.voice_name = "de-DE-Hedda"
    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_filename = "Results/KhanAcademyLinearAlgebra.wav"
    audio_input = speechsdk.audio.AudioOutputConfig(filename=audio_filename)

    # Creates a translation recognizer using and audio file as input.
    recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config, audio_config=audio_input)

    # Prepare to handle the synthesized audio data.
    def synthesis_callback(evt):
        size = len(evt.result.audio)

        if evt.result.reason == speechsdk.ResultReason.SynthesizingAudio:
            print('writing to wav file!!!')
            try:
                with open(f"out_{size}.wav", 'wb') as wavfile:
                    wavfile.write(evt.result.audio)
            except Exception as e:
                print(f'could not write to file: {e}')

        print('AUDIO SYNTHESIZED: {} byte(s) {}'.format(size, '(COMPLETED)' if size == 0 else ''))

    recognizer.synthesizing.connect(synthesis_callback)

    # Starts translation, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognized text as well as the translation.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    print("Say something...")
    result = recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("RECOGNIZED '{}': {}".format(fromLanguage, result.text))
        print("TRANSLATED into {}: {}".format(toLanguage, result.translations['hi']))
    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("RECOGNIZED: {} (text could not be translated)".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("NOMATCH: Speech could not be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("CANCELED: Reason={}".format(result.cancellation_details.reason))
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("CANCELED: ErrorDetails={}".format(result.cancellation_details.error_details))

translate_speech_to_speech()