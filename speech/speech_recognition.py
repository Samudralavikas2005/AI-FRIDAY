# speech/speech_recognition.py
import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def listen_for_command(self):
        with sr.Microphone() as source:
            print("🎤 Listening for command...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)
        try:
            return self.recognizer.recognize_google(audio, language="en-in").lower()
        except Exception as e:
            print("⚠️ (speech recognition) could not understand audio.")
            return None
    
    def listen_for_wake_word(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("🔊 Say 'Friday' to wake me up...")
            while True:
                audio = self.recognizer.listen(source)
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    if "friday" in text or "hey friday" in text:
                        print("✅ Wake-word detected!")
                        return True
                except:
                    continue
