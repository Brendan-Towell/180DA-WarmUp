#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import json

# obtain audio from the microphone
r = sr.Recognizer()

numIncorrect, numCorrect = [0,0],[0,0]
while(1):
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result1 = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + result1)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        

    # recognize speech using Google Cloud Speech
    with open(r'C:\Users\towel\downloads\speech-recognition-test-340720-d3604413ed8e.json') as f:
        data = json.load(f)
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = json.dumps(data)
    try:
        result2 = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        print("Google Cloud Speech thinks you said " + result2)
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
    eval = input("Was the first result correct? y/n or q\n")
    if(eval == 'y'):
        numCorrect[0] += 1
    elif(eval == 'n'):
        numIncorrect[0] += 1
    elif(eval == 'q'):
        break
    eval = input("Was the second result correct? y/n or q\n")
    if(eval == 'y'):
        numCorrect[1] += 1
    elif(eval == 'n'):
        numIncorrect[1] += 1
    elif(eval == 'q'):
        break
    print("Generic cloud API performance: " + str(numCorrect[0]) + " correct and " + str(numIncorrect[0]) + " incorrect")
    print("Specific cloud API performance: " + str(numCorrect[1]) + " correct and " + str(numIncorrect[1]) + " incorrect")
