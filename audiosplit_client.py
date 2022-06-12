import speech_recognition as sr
import requests


def decode_audio(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=2)


    while True:
        while True:
            print('Say something!')
            guess = decode_audio(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        print("I think you said: {}".format(guess["transcription"]))

        # determine if guess is correct and if any attempts remain
        transcription = guess["transcription"].lower().split(' ')

        if set(transcription).isdisjoint(['skip','split','next', 'do', 'go', 'please']):
            print("SPLITTING!")
            x = requests.get('http://192.168.0.32:5000/')
            print(x.text)