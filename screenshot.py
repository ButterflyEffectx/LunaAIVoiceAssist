# screenshot.py

import pyautogui
import psutil
import os
import random
import string
import subprocess
from voice_engine import speak
from listen_engine import listen  # คุณต้องมี listen() แยกไว้อีกไฟล์หนึ่ง หรือ import ตรงจาก main ก็ได้

def random_filename(extension=".png", length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) + extension

def get_picture_path():
    folder = os.path.join(os.path.expanduser("~"), "Pictures", "LunaScreenshots")
    os.makedirs(folder, exist_ok=True)
    return folder

def kill_photo_viewers():
    try:
        # ใช้ PowerShell ปิด Photos.exe โดยตรง
        subprocess.run(
            ["powershell", "-Command", "Get-Process Photos | Stop-Process -Force"],
            check=True
        )
        print("✅ ปิด Photos.exe ด้วย PowerShell แล้ว")
    except subprocess.CalledProcessError as e:
        print("❌ ไม่สามารถปิด Photos.exe ได้:", e)

def capture_screen():
    filename = random_filename()
    folder = get_picture_path()
    path = os.path.join(folder, filename)

    screenshot = pyautogui.screenshot()
    screenshot.save(path)

    print(f"📸 แคปหน้าจอไว้ที่: {path}")
    speak("แคปหน้าจอเรียบร้อยแล้ว")
    return path

def open_image_and_prompt(image_path):
    try:
        subprocess.Popen(["start", image_path], shell=True)  # เปิดภาพ
        speak("เปิดภาพแล้วค่ะ ต้องการปิดภาพเลยไหม")
        command = listen()

        if "ใช่" in command or "ปิด" in command:
            kill_photo_viewers()
            speak("ปิดภาพแล้วค่ะ")
        else:
            speak("รับทราบค่ะ จะไม่ปิดภาพ")
    except Exception as e:
        print(f"❌ เปิดภาพไม่สำเร็จ: {e}")
        speak("ไม่สามารถเปิดภาพได้ค่ะ")
