import speech_recognition as sr

class RecognizeSpeech:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def speech_to_text(self):
        with self.mic as source:
            print("Listening...(say something)")
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                audio = self.recognizer.listen(source)

                try:
                    print("Recognizing...")
                    text = self.recognizer.recognize_google(audio)
                    print(f"You Said : {text}")
                    return text

                except sr.UnknownValueError:
                    print("Voice InAudible : Error")
                    return None

                except sr.RequestError as e:
                    print(f"Request Error : {e}")
                    return None

