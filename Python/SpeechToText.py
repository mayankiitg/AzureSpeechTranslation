import azure.cognitiveservices.speech as speechsdk

#Set up the subscription info for the Speech Service:
speech_key, service_region = "", "eastus"

# Create an instance of a speech config with specified subscription key and service region. Replace with your own subscription key and service region (e.g., "westus").
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Create a recognizer with the given settings. Since no explicit audio config is specified, the default microphone will be used (make sure the audio settings are correct).
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

result = speech_recognizer.recognize_once()

if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))