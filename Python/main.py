from Translation import speech_to_hindi_text
from TextToSpeech import text_to_speech
from Utterance import Utterance

# converted hindi results
utterances = speech_to_hindi_text()
i = 0
print('Converting text to speech')
for utterance in utterances:
    i = i+1
    text_to_speech(utterance.Hindi, f'converted_{i}')
