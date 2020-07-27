import time
import json
import azure.cognitiveservices.speech as speechsdk
from typing import List
from azure.cognitiveservices.speech.audio import AudioConfig
from Utterance import Utterance, WordWithDuration
from Utils import WriteToFile, readSpeechKey, getServiceRegion

### CONFIGURATION #######
folderPath = '../Results/'
fileName = 'speed_khan_academy' #'KhanAcademyLinearAlgebra' #'3blue1brown-channel-trailer'
fileExt = '.wav'
###################

speech_key = readSpeechKey()
service_region = getServiceRegion()

def create_translation_config():
    # Creates an instance of a speech translation config with specified subscription key and service region.
    # Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
    translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key, region=service_region)

    # Sets source and target languages.
    # Replace with the languages of your choice, from list found here: https://aka.ms/speech/sttt-languages
    fromLanguage = 'en-US'
    translation_config.speech_recognition_language = fromLanguage
    translation_config.add_target_language('hi-IN')
    translation_config.request_word_level_timestamps()
    translation_config.output_format = speechsdk.OutputFormat.Detailed
    return translation_config
    # translation_config.set_speech_synthesis_output_format('Riff16Khz16BitMonoPcm')

def create_audio_config():
    audio_config: AudioConfig = AudioConfig(filename=folderPath+fileName+fileExt)
    return audio_config

def getUtteranceFromEvent(evt):
    # englishSentences = evt.result.text.split('.')
    # translatedText = evt.result.translations['hi'].split(u'।')
    parsedWords = json.loads(evt.result.json)['Words']
    english = evt.result.text
    hindi = evt.result.translations['hi']
    words = []
    for word in parsedWords:
        words.append(WordWithDuration(word['Duration'], word['Offset'], word['Word']))
    utteranceDuration = words[-1].offset+ words[-1].duration - words[0].offset
    print(f'Got utterence with {len(words)} words and {utteranceDuration} duration')
    return Utterance(english, hindi, words, utteranceDuration)

def speech_to_hindi_text() -> List[Utterance]:
    translation_config = create_translation_config()
    audio_config = create_audio_config()
     # Creates a translation recognizer using and audio file as input.
    speech_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config, audio_config=audio_config)
    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    english_results = []
    hindi_results = []
    json_results = []
    utterances = []
    def handle_final_result(evt):
        print(f'Completed translation for text: {evt.result.text}')
        # print('evt: {}'.format(evt.result.translations))
        # print('JSON: {}'.format(evt.result.json))
        utterance = getUtteranceFromEvent(evt)
        utterances.append(utterance)
        json_results.append(utterance.words)
        english_results.append(utterance.English)
        hindi_results.append(utterance.Hindi)

    speech_recognizer.recognized.connect(handle_final_result)
    # Connect callbacks to the events fired by the speech recognizer
    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    # speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    # speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.05)

    print("Printing all results:")
    print(english_results)
    print(hindi_results)
    with open(f"../Results/{fileName}_json_results.txt", 'w') as filehandle:
        json.dump(json_results, filehandle, default=lambda o: o.__dict__)
    # with open(f"../Results/{fileName}_utterance.json", 'w') as filehandle:
    #     json.dump(utterances.__dict__, filehandle)
    WriteToFile(english_results, f"../Results/{fileName}_transcribe_eng.txt")
    WriteToFile(hindi_results, f"../Results/{fileName}_translate_hindi.txt")
    return utterances