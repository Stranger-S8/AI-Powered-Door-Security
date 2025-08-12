import speech_recognition as sr
import pyttsx3

class RecognizeSpeech:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.speak_engine = pyttsx3.init()
        self.speak_engine.setProperty('rate', 150)

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

    def text_to_speech(self, text):
        self.speak_engine.say(text)
        self.speak_engine.runAndWait()

if __name__ == "__main__":
    A = RecognizeSpeech()
    A.speech_to_text()



