# listen_engine.py

import speech_recognition as sr
from voice_engine import speak

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 กำลังฟัง...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio, language='th-TH').lower()
            print(f"🗣️ ได้ยินว่า: {command}")
            return command
        except sr.UnknownValueError:
            print("❌ ไม่เข้าใจคำสั่ง")
        except sr.RequestError as e:
            print(f"❌ ข้อผิดพลาดในการเชื่อมต่อ: {e}")
            speak("ระบบกำลังมีปัญหา กรุณาลองใหม่")
        except sr.WaitTimeoutError:
            print("❌ หมดเวลาฟัง")
    return ""
