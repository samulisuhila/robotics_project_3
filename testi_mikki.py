import speech_recognition as sr
from datetime import date
import time
r = sr.Recognizer()
mic = sr.Microphone()


def voice_recog():
    print("microphone setup")
    global value
    while True:
        with mic as source:
            audio = r.listen(source)
            words = r.recognize_google(audio)
            
            if words == "today":
                print(date.today())
                value = 1   
                

            if words == "beer":
                print("Fetching a beer")
                value = 2


            if words == "exit":
                print("...")
                time.sleep(1)
                print("...")
                time.sleep(1)
                print("...")
                time.sleep(1)
                print("Goodbye")
                break
            else:
                print("voice_recog : else")
        return 

#if __name__ == '__main__':
#    voice_recog()
#    time.sleep(5)
#    print("checking words")
#    print(value)